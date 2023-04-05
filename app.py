#!/usr/bin/python3

from flask import Flask, jsonify, abort, request
from models import storage
from models.students import Students
from api.frontend.react import frontend_view
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(frontend_view)
CORS(app)


@app.route("/status", strict_slashes=False)
def status():
    return "In development"

if __name__ == "__main__":
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.run(host="0.0.0.0", debug=True, threaded=True)
