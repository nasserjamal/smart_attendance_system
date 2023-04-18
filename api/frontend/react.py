import base64
import os
import uuid
from flask import Response, jsonify, abort, request, Blueprint
from models import storage
from models.attendance import Attendance
from models.cameras import Cameras
from models.sessions import Sessions
from models.students import Students
from typing import Optional # For typecasting an identified variable
from PIL import Image
from ML import trainer
from controllers import timer_func
import numpy as np
import cv2

frontend_view = Blueprint('frontend_view', __name__, url_prefix="/react")


@frontend_view.route("/status", strict_slashes=False)
def get_status():
    return Response("In development", 200)


# Students


@frontend_view.route("/students", strict_slashes=False)
def get_students():
    return jsonify([std.get_json("name", "reg_no", "id") for std in storage.get_all(Students)])


@frontend_view.route("/student", methods=['POST'], strict_slashes=False)
def post_student():
    try:
        req = request.get_json()
    except:
        abort(404, "Not json format")
    arg_list = ['name', 'reg_no']
    for arg in arg_list:
        if arg not in req.keys():
            abort(404, f"arg {arg} not found")
    student = Students(**req)
    storage.new(student)
    return jsonify("status: OK")

@frontend_view.route("/student/<student_id>", methods=['DELETE'], strict_slashes=False)
def delete_student(student_id):
    student = storage.get(Students, "id", student_id)
    if (student == None):
        return Response("Not found", 404)
    storage.delete(student)
    return Response("OK", 204)


@frontend_view.route("/student", methods=['PUT'], strict_slashes=False)
def update_student():
    try:
        req = request.get_json()
    except:
        abort(404, "Not json format")
    arg_list = ['name', 'reg_no', 'id']
    for arg in arg_list:
        if arg not in req.keys():
            print("args not found")
            abort(404, f"arg {arg} not found")
    student: Optional[Students] = storage.get(Students, "id", req["id"])
    if (student == None):
        return Response("Not found", 404)
    student.update_object(**req)
    storage.save()
    return Response("OK", 204)


# Sessions


@frontend_view.route("/sessions", strict_slashes=False)
def get_sessions():
    json_obj = []
    for session, camera  in storage.get_all(Sessions, Cameras):
        temp_session = session.get_json("id","name", "start_time", "end_time")
        temp_session = {"session_"+key:val for key, val in temp_session.items()}
        temp_camera = camera.get_json("id","name","ip")
        temp_camera = {"camera_"+key:val for key, val in temp_camera.items()}
        json_obj.append({**temp_session, **temp_camera})
    return jsonify(json_obj)


@frontend_view.route("/session", methods=['POST'], strict_slashes=False)
def post_session():
    try:
        req = request.get_json()
    except:
        abort(404, "Not json format")
    print(f"Date sent over is {req['start_time']}")
    arg_list = ['name', 'start_time', 'end_time', 'camera_id']
    for arg in arg_list:
        if arg not in req.keys():
            print(f"arg {arg} not found")
            abort(404, f"arg {arg} not found")
    if storage.get(Cameras, "id", req["camera_id"]) is None:
        print("Cam id not found")
        abort(404, "Cam id not found")
    session = Sessions(**req)
    print(session.name)
    storage.new(session)
    timer_func.schedule_task(session)
    return jsonify("status: OK")

@frontend_view.route("/session/<session_id>", methods=['DELETE'], strict_slashes=False)
def delete_session(session_id):
    session = storage.get(Sessions, "id", session_id)
    if (session == None):
        return Response("Not found", 404)
    storage.delete(session)
    return Response("OK", 204)


@frontend_view.route('/session_report/<int:session_id>', methods=['GET'], strict_slashes=False)
def get_session_report(session_id):
    session = storage.get(Sessions, "id", session_id)
    if session is None:
        print("Error! 404 Session not found")
        abort(404, "Session not found")

    result = []
    report_data = storage.get_all(Attendance, Students, Sessions)
    for data in report_data:
        att, std, ses = data
        if ses.id == session_id:
            temp_att = att.get_json("id", "start_time", "end_time")
            temp_att = {"attendance_"+key:val for key, val in temp_att.items()}
            temp_std = std.get_json("id", "name", "reg_no")
            temp_std = {"student_"+key:val for key, val in temp_std.items()}
            temp_ses = ses.get_json("id", "name", "start_time", "end_time")
            temp_ses = {"session_"+key:val for key, val in temp_ses.items()}
            result.append({**temp_att, **temp_ses, **temp_std})
    return jsonify(result), 200


@frontend_view.route("/session/<session_id>", methods=['PUT'], strict_slashes=False)
def update_session(session_id):
    session: Optional[Sessions] = storage.get(Sessions, "id", session_id)
    if (session == None):
        return Response("Not found", 404)
    try:
        req = request.get_json()
    except:
        abort(404, "Not json format")
    session.update_object(**req)
    storage.save()
    timer_func.schedule_task(session)
    return Response("OK", 204)


# Attendance

@frontend_view.route("/attendance/<int:session_id>", strict_slashes=False)
def get_attendance(session_id):
    json_obj = []
    for attendance, session  in storage.get_all(Attendance, Sessions):
        temp_session = session.get_json("id","name")
        temp_session = {"session_"+key:val for key, val in temp_session.items()}
        temp_attendance = attendance.get_json("id","name","ip")
        temp_attendance = {"attendance_"+key:val for key, val in temp_attendance.items()}
        json_obj.append({**temp_session, **temp_attendance})
    return jsonify(json_obj)


# New student registration

@frontend_view.route('/upload', methods=['POST'])
def submit_form():
    name = request.form['name']
    reg_no = request.form['reg_no']
    images = request.files.getlist('images')
    if(len(images) == 0):
        return jsonify(error="No images passed"), 400
    if(len(images) < 4):
        return jsonify(error="Please provide more images. Ateast 4"), 400
    student = storage.get(Students, "reg_no", reg_no)
    if student != None:
        return jsonify(error=f"A student with registration no {reg_no} has already been registered"), 400
    for img_data in images:
        # Read the content of the file as bytes
        file_bytes = img_data.read()
        
        # Convert the bytes to an OpenCV image
        img_data = np.frombuffer(file_bytes, dtype=np.uint8)
        img = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
        
        isSuccess, msg = trainer.has_face(img)
        if not isSuccess:
            return jsonify(error=f"{img_data.filename} : {msg}"), 400
    student = Students(**{"name":name, "reg_no":reg_no})
    storage.new(student)
    for img_data in images:
        img = Image.open(img_data)
        isSuccess, msg = trainer.face_to_csv("", int(student.id), np.array(img))
        if not isSuccess:
            return jsonify(error=f"{img_data.filename} : {msg}"), 400
    trainer.train_model()
    return jsonify({"status":"Success: Face added to database"}), 200

# Cameras
@frontend_view.route("/cameras", strict_slashes=False)
def get_cameras():
    return jsonify([std.get_json("name", "id") for std in storage.get_all(Cameras)])


# Reports
@frontend_view.route("/reports", strict_slashes=False)
def get_reports():
    json_obj = []
    for attendance, student, session  in storage.get_all(Attendance, Students,Sessions):
        temp_attendance = attendance.get_json("id", "start_time", "end_time")
        temp_attendance = {"attendance_"+key:val for key, val in temp_attendance.items()}
        temp_session = session.get_json("id","name")
        temp_session = {"session_"+key:val for key, val in temp_session.items()}
        temp_student = student.get_json("id","name","reg_no")
        temp_student = {"student_"+key:val for key, val in temp_student.items()}
        json_obj.append({**temp_attendance, **temp_session, **temp_student})
    return jsonify(json_obj)

@frontend_view.route('/image_check', methods=['POST'])
def image_check():
    image_data = request.json.get('image')
    image_format, image_str = image_data.split(';base64,')
    ext = image_format.split('/')[-1]
    UPLOAD_FOLDER = 'uploads'

    # Decode the base64 image
    decoded_image = base64.b64decode(image_str)

    success, msg = trainer.has_face(img_data=trainer.cv2.imdecode(np.frombuffer(decoded_image, dtype=np.uint8), trainer.cv2.IMREAD_COLOR))
    print(f"success is {success}")
    return jsonify({"valid": success, "message":msg})


# Settings
@frontend_view.route('/reset')
def reset_system():
    print("Request received")
    data = request.args.get('data')

    if data == 'yUTF56':
        response = jsonify(success=True)
        response.status_code = 200
    else:
        response = jsonify(success=False)
        response.status_code = 404
        return response
    
    print("Now dropping all the tables")
    storage.drop_all_tables()
    print("Done dropping all tables")
    trainer.reset_model()


    return response
