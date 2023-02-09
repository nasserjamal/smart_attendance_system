#!/usr/bin/python3
"""Testing file"""

import models
from datetime import time
from models import storage
from models.sessions import Sessions
from models.attendance import Attendance
from models.students import Students

#create new student
# student1 = Students()
# student1.name = 'Dhulkifli'
# student1.student_id = 1
# student1.reg_no = 'MPE/03/18'
# student2 = Students()
# student2.name = 'Nasser'
# student2.student_id = 2
# student2.reg_no = 'TLE/20/18'
# student3 = Students()
# student3.name = 'Pigabuff Al Kindii'
# student3.student_id = 3
# student3.reg_no = 'EC/03/18'
student4 = Students()
student4.name = 'Bolton'
student4.reg_no = 'Bithwa/05/18'

# #create new session
# session1 = Sessions()
# session1.session_id = 1
# session1.name = 'MPE 512'
# session1.start_time = time(9, 0)
# session1.end_time = time(10, 0)

#create new attendance
attendance3 = Attendance()
attendance3.student_id = 3
attendance3.session_id = 1
attendance3.start_time = time(9, 0)
attendance3.end_time = time(10, 0)
attendance3.id = 3


# models.storage.reload()
models.storage.new(student4)
# models.storage.new(session1)
# models.storage.new(attendance3)
# models.storage.save()
models.storage.delete(student4)
models.storage.save()