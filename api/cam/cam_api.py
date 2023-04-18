from pathlib import Path
from flask import Flask, request, Response, Blueprint
from models.cameras import Cameras
from models import storage
import base64
from werkzeug.utils import secure_filename
from controllers import image_func
from controllers.students_data_processor import Students_data_processor

cam_view = Blueprint('cam_view', __name__, url_prefix="/cam")


@cam_view.route('/init', methods=['POST'])
def camInit():
    name = request.headers['X-Cam-Name']
    ip = request.remote_addr
    if storage.get(Cameras, "ip", ip) is None:
        new_cam = Cameras()
        new_cam.name = name
        new_cam.ip = ip
        storage.new(new_cam)
        print("New camera has been stored")

    return Response(status=200)


@cam_view.route('/upload', methods=['POST'])
def receive_image():
    print("Now processing the request")
    data = request.get_data()
    start_index = 0
    processor = Students_data_processor(request.headers.get("X-Session-Id"))

    while start_index < len(data):
        start_index = data.find(b'Content-Disposition:', start_index)
        if start_index == -1:
            break

        end_index = data.find(b'\r\n\r\n', start_index)
        start_index = end_index + 4
        end_index = data.find(b'\r\n--123456789', start_index)
        if end_index == -1:
            end_index = len(data)

        image_data = data[start_index:end_index]
        students_data = image_func.process_image(image_data)
        image_func.saveImage(image_data)
        if not students_data:
            continue
        print(f"Students data are {students_data}")
        processor.add_data(students_data)
        start_index = end_index
    attendances = processor.get_student_list()
    print(attendances)
    # if len(attendances) == 0:
    #     print("Attendances is 0")
    #     pass
    # else:
    for attendance in attendances:
        print("SToring")
        storage.new(attendance)
    return 'Images uploaded and saved successfully.'
