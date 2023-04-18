from flask import request
from datetime import datetime, timedelta
import time
import requests
from models import storage
from models.sessions import Sessions
from models.cameras import Cameras
import schedule
import pytz
from typing import Optional

no_captures = 10
n_minutes = 5
running_jobs = {}

def send_image_capture_request(no_captures, ip, session_id):
    remote_server_url = "http://"+ip+":80/capture"
    response = "Err!"
    try:
        response = requests.get(remote_server_url, params={'i': session_id, 'c': no_captures})
    except:
        print("Error! Could not connect to the camera")
    return response

def call_send_get_request_periodically(session_id, no_captures, n_minutes, end_time, ip, *args, **kwargs):
    print(f"Time has recahed. I will be calling {ip} to capture {no_captures} images for session {session_id} untill {end_time} for {n_minutes} minutes")
    schedule.cancel_job(running_jobs.get(session_id))
    while datetime.now() < end_time:
        print("Now sending request for images")
        response = send_image_capture_request(no_captures, ip,session_id)
        print(f"Going to sleep {response}")
        time.sleep(n_minutes * 60)

        
def run_scheduling_tasks():
    sessions = storage.get_all_greater(Sessions, "end_time", utc_timenow())
    Optional[Sessions]:session
    for session in sessions:
        cam = storage.get(Cameras, "id", session.camera_id)
        print(f"Cam ip is {cam.ip}")
        start_time = utc_to_local(session.start_time)
        end_time = utc_to_local(session.end_time)

        time_remaining = start_time - datetime.now()
        time_remaining = int(time_remaining.total_seconds())
        job = schedule.every(time_remaining).seconds.do(call_send_get_request_periodically, session.id, no_captures, n_minutes, end_time, cam.ip)
        running_jobs[session.id] = job
        print(f"Will run {session.name} at {start_time} now is {datetime.now()}")

    while True:
        schedule.run_pending()
        time.sleep(1)

def schedule_task(session):
    if string_to_datetime(session.end_time) <= utc_timenow():
        print("Time has passed. Cannot schedule")
        return
    if running_jobs.get(session.id) is not None:
        schedule.cancel_job(running_jobs.get(session.id))
    cam = storage.get(Cameras, "id", session.camera_id)
    start_time = utc_to_local(string_to_datetime(session.start_time))
    end_time = utc_to_local(string_to_datetime(session.end_time))

    time_remaining = start_time - datetime.now()
    time_remaining = int(time_remaining.total_seconds())
    job = schedule.every(time_remaining).seconds.do(call_send_get_request_periodically, session.id, no_captures, n_minutes, end_time, cam.ip)
    running_jobs[session.id] = job

def utc_timenow():
    local_time = datetime.now()
    local_tz = pytz.timezone('Africa/Nairobi')
    utc_time = local_tz.localize(local_time).astimezone(pytz.utc)
    return utc_time

def utc_to_local(time):
    time = time.replace(tzinfo=None)
    utc_dt = pytz.utc.localize(time)
    local_tz = pytz.timezone('Africa/Nairobi')
    local_dt = utc_dt.astimezone(local_tz)
    return local_dt.replace(tzinfo=None)

def string_to_datetime(date_string):
    format_string = "%Y-%m-%d %H:%M:%S.%f"
    datetime_object = datetime.strptime(date_string, format_string)
    timezone = pytz.utc
    datetime_object = timezone.localize(datetime_object)
    return datetime_object



