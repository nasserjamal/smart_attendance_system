#!/usr/bin/python3

from flask import Flask, jsonify, abort, request
from models import storage
from models.students import Students
from api.frontend.react import frontend_view
from api.cam.cam_api import cam_view
from controllers import timer_func
from flask_cors import CORS
import threading


app = Flask(__name__)
app.register_blueprint(frontend_view)
app.register_blueprint(cam_view)
CORS(app)


@app.route("/status", strict_slashes=False)
def status():
    return "In development"

if __name__ == "__main__":
    # Scheduler
    scheduler_thread = threading.Thread(target=timer_func.run_scheduling_tasks)
    scheduler_thread.start()

    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.run(host="0.0.0.0", debug=False, threaded=True)
