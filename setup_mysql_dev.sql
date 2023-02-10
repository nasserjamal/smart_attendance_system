-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS smart_attendance;
CREATE USER IF NOT EXISTS 'smart_attendance_dev'@'localhost' IDENTIFIED BY '12345';
GRANT ALL PRIVILEGES ON `smart_attendance`.* TO 'smart_attendance_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'smart_attendance_dev'@'localhost';
FLUSH PRIVILEGES;
