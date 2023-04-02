#!/usr/bin/python3

import models
from flask import Flask, jsonify, abort, request
from models import storage
from models.students import Students
app = Flask(__name__)


@app.route("/home", strict_slashes=False)
def home():
    return "In development"

@app.route("/students", strict_slashes=False)
def get_students():
    return jsonify([std.get_json("name", "reg_no", "student_id", "course") for std in storage.get_all(Students)])

@app.route("/student", methods=['POST'], strict_slashes=False)
def post_student():
    try:
        req = request.get_json()
    except:
        abort(404, "Not found ja3be")
    arg_list = ['name']#, 'reg_no', 'gender', 'phone_no', 'year_of_study', 'department', 'course']
    for arg in arg_list:
        if arg not in req.keys():
            abort(404, f"arg {arg} not found")
    student = Students()
    student.name = 'Nasser'
    student.reg_no = 'TLE/20/18'
    student.gender = 'M'
    student.phone_no = '07130021458'
    student.year_of_study = 5
    student.department = 'TLE'
    student.course = 'Ruto'
    storage.new(student)
    return jsonify("status: OK")

if __name__ == "__main__":
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.run(host="0.0.0.0", debug=True, threaded=True)
