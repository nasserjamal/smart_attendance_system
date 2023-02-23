from flask import Flask
from models import storage
from models.students import Students
app = Flask(__name__)


@app.route("/home", strict_slashes=True)
def home():
    return "In development"

@app.route("/students", strict_slashes=True)
def get_students():
    return [std.get_json("name", "reg_no", "id", "course") for std in storage.all(Students)]

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, threaded=True)
