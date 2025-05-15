from mtcnn import MTCNN
import cv2 
import numpy as np

class FaceDetector:
    def __init__(self):
        self.dectector = MTCNN()

    def detect_and_crop(self, image):
        results = self.dectector.detect_faces(image)

        if not results:
            return None
        
        x, y, width, height = results[0]['box']
        x, y = abs(x), abs(y)
        cropped_image = image[y:y+height, x:x+width]
        return cv2.resize(cropped_image, (160, 160))
    