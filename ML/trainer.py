import cv2
import numpy as np
from ML import face_cascade, faces_csv, trained_model, recognizer
import math

def face_to_csv(path, id):
    """
    Detects faces in an image and Converts the faces to a numpy array then stores it in a csv file
    Args: 
        img: Path to the image
    returns false if no face was found, otherwise returns true
    """
    img = cv2.imread(path)
    if img is None:
        print("Error: Could not find the image. Check the path to the image passed")
        return False
    if type(id) is not int:
        print("Id must be an int")
        return False

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img_gray, scaleFactor=1.5, minNeighbors=5)
    if len(faces) == 0:
        print("No faces detected")
        return False
    for x, y, w, h in faces:
        roi = img_gray[y:y+h, x:x+w]
        # In the microprocessor add a margin of 50
    face_array = np.array(roi)
    flattened_faces = face_array.flatten()
    with open(faces_csv,'a+') as myFile:
        flattened_faces = np.append(id, flattened_faces)
        flattened_faces = np.append(flattened_faces, '\n')
        flattened_faces.tofile(myFile, sep=",", format='%s')


def train_model():
    """
    Train the faces model using data from faces.csv
    if the model is successfully trained, shouldreturn true
    Else the function returns false
    """
    try:
        data = np.genfromtxt(faces_csv, delimiter=",")
    except:
        print("Faces database not found. Ensure you have a csv file")
        return False
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


def show_roi(path, id):
    img = cv2.imread(path)
    if img is None:
        print("Error: Could not find the image. Check the path to the image passed")
        return False
    if type(id) is not int:
        print("Id must be an int")
        return False

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img_gray, scaleFactor=1.3, minNeighbors=5)
    print(len(faces))
    if len(faces) == 0:
        print("No faces detected")
        return False
    for x, y, w, h in faces:
        roi = img_gray[y:y+h, x:x+w]
        cv2.imshow("Region of interest", roi)
    cv2.waitKey(9000)

def reset_model():
    """Deletes all the faces in the csv file"""
    with open(faces_csv,'w+') as myFile:
        flattened_faces = np.arange(1, 100, 1)
        flattened_faces = np.append("id", flattened_faces)
        flattened_faces = np.append(flattened_faces, '\n')
        flattened_faces.tofile(myFile, sep=",", format='%s')