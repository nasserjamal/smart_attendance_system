from flask import Response, jsonify, abort, request, Blueprint
from models import storage
from models.attendance import Attendance
from models.cameras import Cameras
from models.sessions import Sessions
from models.students import Students
from typing import Optional # For typecasting an identified variable
from PIL import Image
from ML import trainer
import numpy as np

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


@frontend_view.route("/student/<student_id>", methods=['PUT'], strict_slashes=False)
def update_student(student_id):
    student: Optional[Students] = storage.get(Students, "id", student_id)
    if (student == None):
        return Response("Not found", 404)
    try:
        req = request.get_json()
    except:
        abort(404, "Not json format")
    student.update_object(**req)
    storage.save()
    return Response("OK", 204)


# Sessions


@frontend_view.route("/sessions", strict_slashes=False)
def get_sessions():
    json_obj = []
    for session, camera  in storage.get_all(Sessions, Cameras):
        print("Iterr")
        temp_session = session.get_json("id","name")
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
    arg_list = ['name', 'start_time', 'end_time', 'camera_id']
    for arg in arg_list:
        if arg not in req.keys():
            abort(404, f"arg {arg} not found")
    if storage.get(Cameras, "id", req["camera_id"]) is None:
        abort(404, "Cam id not found")
    session = Sessions(**req)
    print(session.name)
    storage.new(session)
    return jsonify("status: OK")

@frontend_view.route("/session/<session_id>", methods=['DELETE'], strict_slashes=False)
def delete_session(session_id):
    session = storage.get(Sessions, "id", session_id)
    if (session == None):
        return Response("Not found", 404)
    storage.delete(session)
    return Response("OK", 204)


@frontend_view.route("/session/<session_id>", methods=['PUT'], strict_slashes=False)
def update_session(session_id):
    session: Optional[Students] = storage.get(Students, "id", session_id)
    if (session == None):
        return Response("Not found", 404)
    try:
        req = request.get_json()
    except:
        abort(404, "Not json format")
    session.update_object(**req)
    storage.save()
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
        return jsonify({"status":"No images passed"}), 200
    if(len(images) < 4):
        return jsonify({"status":"Please provide more images. Ateast 4"}), 200
    student = storage.get(Students, "reg_no", reg_no)
    if student != None:
        return jsonify({"status":f"A student with registration no {reg_no} has already been registered"}), 200
    for img_data in images:
        img = Image.open(img_data)
        isSuccess, msg = trainer.has_face(np.array(img))
        if not isSuccess:
            return jsonify({"status":f"{img_data.filename} : {msg}"}), 200
    student = Students(**{"name":name, "reg_no":reg_no})
    storage.new(student)
    for img_data in images:
        img = Image.open(img_data)
        isSuccess, msg = trainer.face_to_csv("", int(student.id), np.array(img))
        if not isSuccess:
            return jsonify({"status":f"{img_data.filename} : {msg}"}), 200
    return jsonify({"status":"Success: Face added to database"}), 200
