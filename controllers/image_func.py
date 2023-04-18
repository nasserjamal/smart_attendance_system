import os
import numpy as np
import cv2
from ML import trainer

images_folder = 'images'

def saveImage(image_data):
    file_count = len(os.listdir(images_folder))
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)
    filename = os.path.join(images_folder, f'image{file_count + 1}.jpg')
    with open(filename, 'wb') as f:
        f.write(image_data)

def process_image(image_data):
    decoded_image = cv2.imdecode(np.frombuffer(image_data, dtype=np.uint8), cv2.IMREAD_COLOR)
    data = trainer.get_faceid(img_data=decoded_image)
    return data
