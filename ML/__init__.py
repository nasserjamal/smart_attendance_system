import cv2
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
faces_csv = "faces.csv"
trained_model = "trainer.yml"
recognizer = cv2.face.LBPHFaceRecognizer_create()
