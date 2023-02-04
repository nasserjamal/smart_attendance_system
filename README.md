# Smart Attendance System
Track attendance with ease and accuracy using face recognition.
## Team
Nasser Jamal: Backend developer. Very good with backends
Dhulkifli Abbas: Frontend developer. Very good with frontends
## Technologies
List of technologies necessary to complete the project:
Face detection and recognition libraries: OpenCV, Dlib, and/or Face-API.js
Programming languages: Python and/or JavaScript
Platforms: Windows, Linux, or MacOS
Frameworks: TensorFlow and/or Keras
Hardware: Webcam, Raspberry Pi, or similar device
Books and resources: "Mastering OpenCV 4 with Python" by Alberto Fernández Villán and Prateek Joshi, "Deep Learning for Computer Vision" by Adrian Rosebrock, and online tutorials and documentation for the chosen technologies.
Option 1: Face detection and recognition libraries:
Chosen technology: OpenCV
Alternate option: Dlib
Trade-offs: OpenCV has a wider range of functions and is more user-friendly, but Dlib has a smaller footprint and is faster for certain tasks.
Decision: OpenCV was chosen for its user-friendliness and wider range of functions, as it would make it easier for the team to implement and test various face detection and recognition techniques.
Option 2: Programming languages:
Chosen technology: Python
Alternate option: JavaScript
Trade-offs: Python is a more versatile language with a larger library of machine learning and computer vision libraries. JavaScript is a more common web programming language and can be used in the browser.
Decision: Python was chosen for its versatility and larger library of machine learning and computer vision libraries, as it would make it easier for the team to implement and test various face detection and recognition techniques. JavaScript was considered as an alternate option, but ultimately not chosen because the project would not require browser-based functionality.
## Challenge
The problem the Portfolio Project is intended to solve is to create an attendance system that uses face detection and recognition technology to accurately track attendance in a fast and efficient manner. The current manual attendance system is time-consuming and prone to errors, and the use of face recognition technology aims to automate the process and improve accuracy.
The Portfolio Project will not solve the problem of identifying individuals who try to cheat the system by using someone else's face, although the system will have some built-in measures to detect and prevent that.
The Portfolio Project will help organizations and educational institutions that require an efficient and accurate attendance tracking system. The users of this system will be the employees, students, and administrators of the organization or institution.
This project is not specific to a particular locale and can be used in various locations and settings such as schools, offices, and factories. The use of face recognition technology is a globally recognized technology, and the system can be adapted to the specific needs of different locales.
## Risks
### Technical Risks:
The system may not be able to recognize faces accurately in certain lighting conditions or when the subject is wearing certain types of face coverings. Potential Impact: Misidentification of individuals and inaccurate attendance records. Safeguards/Alternatives: Testing the system under various lighting conditions and implementing image processing techniques to improve recognition accuracy.
The system may not be able to handle large numbers of users at once. Potential Impact: Slow performance and errors in attendance tracking. Safeguards/Alternatives: Optimizing the system's architecture and implementing load balancing techniques.
### Non-technical Risks:
Privacy concerns. Potential Impact: Loss of trust and negative public perception. Strategies: Implementing strict security measures, such as encryption and access control, and being transparent about data collection and usage.
Resistance to change from employees or students. Potential Impact: Reduced adoption and effectiveness of the system. Strategies: Providing training and support for users, communicating the benefits of the system, and involving stakeholders in the implementation process.
Budget constraints. Potential Impact: Lack of resources to implement and maintain the system. Strategies: Careful cost planning and budgeting, seeking funding from outside sources, and identifying cost-saving measures.
It's important to note that even though risks can't be completely eliminated, it's possible to mitigate them by implementing appropriate safeguards and alternatives. The key is to identify the risks, evaluate their potential impact, and develop a plan to address them effectively.
Infrastructure
Branching and merging in the team's repository: Our team will be using the GitHub flow as our branching and merging strategy. This involves creating a new branch for each feature or bug fix, and merging it back into the main branch (usually called "master") once it has been reviewed and approved by the team. This allows for multiple people to work on different aspects of the project simultaneously without affecting the main branch, and also makes it easy to roll back changes if necessary. We will also use pull request process for review and approvals.
Deployment strategy: We will be using a Continuous Integration and Continuous Deployment (CI/CD) pipeline for deployment. This involves automatically building, testing, and deploying code changes as soon as they are committed to the repository. We'll use GitHub actions or Jenkins as our CI/CD tool, which will help us to build and test the code, then deploy it to the production environment if all the tests passed.
Populating the app with data: The app will be populated with data by using a combination of manual input and automated data import. The initial data set will be entered manually by the admin. Additionally, we will implement an automated data import process, which will allow us to easily import data from external sources such as CSV or Excel files.
Tools, automation, and process for testing: We will be using a combination of unit tests, integration tests, and acceptance tests to ensure the quality of the code. We'll use Jest, pytest, and Selenium for testing. We will also use Test-Driven Development (TDD) process to write test cases before the implementation. This will help to catch any bugs early in the development process. Additionally, we will use automated testing tools such as CodeClimate, SonarQube, or similar to check for code quality, maintainability, and security.
## Existing solutions
List of similar products or solutions that currently exist:
Facial recognition-based attendance systems
QR code-based attendance systems
Biometric-based attendance systems
### Similarities and Differences:
Facial recognition-based attendance systems: These systems use a camera to capture an image of a person's face and then use facial recognition algorithms to match the image to a database of enrolled individuals. Similarities include the use of facial recognition technology and the ability to automate attendance tracking. Differences include potential issues with recognition accuracy and privacy concerns.
QR code-based attendance systems: These systems use QR codes to track attendance. Users scan the QR code with their mobile devices, and the system records their attendance. Similarities include the ability to automate attendance tracking. Differences include the need for each user to have a mobile device with a QR code reader and the potential for QR codes to be copied or shared.
Biometric-based attendance systems: These systems use biometric technologies such as fingerprint or iris recognition to track attendance. Similarities include the ability to automate attendance tracking. Differences include the potential issues with recognition accuracy and the need for specialized hardware.
In this case, the project we are developing is an attendance system using face detection and recognition technology. This is a common solution for attendance tracking as it is efficient and accurate. Other solutions include QR code-based attendance systems and biometric-based attendance systems, but face detection and recognition technology is more commonly used and has fewer limitations.

## Architecture

Web architecture						Data flow

## APIs and Methods:
/api/attendance GET: Returns a list of all the recorded attendances 
/api/students GET: Returns a list of all the registered students in the system POST: Adds a new student to the system
/api/Sessions GET: Returns a list of all the registered sessions in the system POST: Adds a new session to the system
/api/log_session POST: Takes a json body with the following data
Frame_id: The index of the frame processed
Time: Time when the video was captured
Image: An array of images with faces and an id for each face
Data Model


## User Stories
- As a teacher, I want to be able to take attendance by simply capturing the image of each student in the class, so that I can save time and ensure accuracy in taking attendance.
- As a student, I want to be able to view my attendance record easily, so that I can keep track of my attendance.
- As a administrator, I want to be able to generate reports on the attendance of all students, so that I can track overall attendance patterns and identify areas for improvement.
- As a teacher, I want to be able to add new students to the system easily, so that I can keep the student database up to date.
- As a student, I want the system to provide instant feedback on whether my attendance has been recorded or not, so that I can ensure my attendance is being recorded accurately.

