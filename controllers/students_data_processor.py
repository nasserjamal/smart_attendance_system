from models.attendance import Attendance
from models import storage
from datetime import datetime
from controllers import timer_func
from models.sessions import Sessions

class Students_data_processor:
    min_appearance = 0.5
    min_confidence = 0


    def __init__(self, session_id):
        self.students_detected = {}
        self.session_id = session_id
        # self.session = storage.get(Sessions)

    def add_data(self, data):
        for std_data in data:
            if (std_data.get("id") in self.students_detected):
                self.students_detected[std_data.get("id")]['count'] += 1
            else:
                std_data['count'] = 1
                self.students_detected[std_data.get("id")] = std_data
    
    def get_student_list(self):
        attendances = []
        for std in self.students_detected.values():
            if not self.is_data_valid(std):
                continue
            att = storage.get(Attendance, **{"student_id":std.get('id'), "session_id": self.session_id})
            if att is None:
                att = Attendance()
                att.student_id = std.get('id')
                att.session_id = self.session_id
                att.start_time = timer_func.utc_timenow()
            att.end_time = timer_func.utc_timenow()
            attendances.append(att)

        print(attendances)
        return attendances
    
    def is_data_valid(self, data) -> bool:
        if data['count'] < self.min_appearance * len(self.students_detected):
            return False
        return True
    
    def no_students_found(self):
        pass

    
