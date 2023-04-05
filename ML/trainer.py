import cv2
import numpy as np
from ML import face_cascade, faces_csv, trained_model, recognizer
import math

scale = 300
scaleFactor=1.1
minNeighbors=5

def face_to_csv(path, id, img_data=None):
    """
    Detects faces in an image and Converts the faces to a numpy array then stores it in a csv file
    Args: 
        img: Path to the image
    returns false if no face was found, otherwise returns true
    """
    if img_data.all() == None:
        img = cv2.imread(path)
    else:
        img = img_data
    if img is None:
        return False, "Error! Could not open the image"
    if type(id) is not int:
        return False, "Id must be an int"

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img_gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors)
    if len(faces) == 0:
        return False, "No faces detected"
    for x, y, w, h in faces:
        roi = img_gray[y:y+h, x:x+w]
    roi = scale_roi(roi)
    face_array = np.array(roi)
    flattened_faces = face_array.flatten()
    with open(faces_csv,'a+') as myFile:
        flattened_faces = np.append(id, flattened_faces)
        flattened_faces = np.append(flattened_faces, '\n')
        flattened_faces.tofile(myFile, sep=",", format='%s')
    return True, "success"


def train_model():
    """
    Train the faces model using data from faces.csv
    if the model is successfully trained, shouldreturn true
    Else the function returns false
    """
    #try:
    data = np.genfromtxt(faces_csv, delimiter=",")
    #except Exception:
    #    print(f"Faces database not found. Ensure you have a csv file")
    #    return False
    labels = data[1:, 0].astype(np.int64)
    faces = data[1:, 1:-1].astype(np.uint8)
    faces = [face.reshape((int(math.sqrt(len(face))), int(math.sqrt(len(face))))) for face in faces]
    try:
        recognizer.train(faces, labels)
        recognizer.save(trained_model)
    except:
        print("Error: There was an error training the model")
        return False
    return True


def show_roi(path):
    img = cv2.imread(path)
    if img is None:
        print("Error: Could not find the image. Check the path to the image passed")
        return False

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img_gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors)
    print(f"No of faces is {len(faces)}")
    if len(faces) == 0:
        print("No faces detected")
        return False
    i = 0
    for x, y, w, h in faces:
        roi = img_gray[y:y+h, x:x+w]
        roi = scale_roi(roi)
        cv2.imshow(f"Region of interest{i}", roi)
        i=i+1
    cv2.waitKey(9000)


def reset_model():
    """Deletes all the faces in the csv file"""
    with open(faces_csv,'w+') as myFile:
        flattened_faces = np.zeros(scale * scale)
        flattened_faces = np.append("id", flattened_faces)
        flattened_faces = np.append(flattened_faces, '\n')
        flattened_faces.tofile(myFile, sep=",", format='%s')


def realtime_facedetect():
    """Prototype recognizes faces in realtime"""
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def realtime_facerecognition():
    recognizer.read(trained_model)
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_gray = scale_roi(roi_gray)
            label, confidence = recognizer.predict(roi_gray)
            cv2.putText(frame, str(label), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
            cv2.putText(frame, str(confidence), (x+w-50, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def realtime_faceregistration():
    """Registers a face in realtime. Press c to register"""
    print("To capture the frame press 'c'")
    id = input("enter the face id you want to register: ")
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            roi = gray[y:y+h, x:x+w]
        cv2.imshow('Frame', frame)
        capture = cv2.waitKey(1)
        if capture == ord('c'):
            if len(faces) == 1:
                roi = scale_roi(roi)
                face_array = np.array(roi)
                flattened_faces = face_array.flatten()
                with open(faces_csv,'a+') as myFile:
                    flattened_faces = np.append(id, flattened_faces)
                    flattened_faces = np.append(flattened_faces, '\n')
                    flattened_faces.tofile(myFile, sep=",", format='%s')
                print("Face successfully saved")
            else:
                print("Error: Multiple faces detected. Ensure you only have one face!!!")
                
        elif capture == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def has_face(img_data=None, path=""):
    if img_data.all() == None:
        img = cv2.imread(path)
    else:
        img = img_data
    if img is None:
        return False, "Invalid image"
    recognizer.read(trained_model)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img_gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors)
    if len(faces) == 0:
        return False, "No face detected"
    if len(faces) == 1:
        return True, "Image detected"
    else:
        return False, f"{len(faces)} faces detected"


def get_faceid(path):
    """
    Returns an array of tuples containing face id and position of face detected
    """
    img = cv2.imread(path)
    if img is None:
        print("Error: Could not find the image. Check the path to the image passed")
        return False

    result = []
    recognizer.read(trained_model)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img_gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors)
    if len(faces) == 0:
        print("No faces detected")
        return False
    for x, y, w, h in faces:
        roi = img_gray[y:y+h, x:x+w]
        roi = scale_roi(roi)
        label, confidence = recognizer.predict(roi)
        result.append((label, (x, y)))
    return result


def scale_roi(roi):
    return cv2.resize(roi, (scale, scale))
