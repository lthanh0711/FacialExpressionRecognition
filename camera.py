import cv2
from model import FacialExpressionModel
import numpy as np
import os

facec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
model = FacialExpressionModel("model.json", "model_weights.h5")
font = cv2.FONT_HERSHEY_SIMPLEX
unused_vid = []

class VideoCamera(object):
    def __init__(self):
        
        if len(unused_vid) > 1:
            print(unused_vid)
            os.remove(os.path.join("./videos", unused_vid[0]))
            unused_vid.pop(0)

        for f in os.listdir("./videos"):
            if f != "facial_exp.mkv" and f not in unused_vid:
                self.video = cv2.VideoCapture(os.path.join("./videos", f))
                unused_vid.append(f)
                return
        
        self.video = cv2.VideoCapture("./videos/facial_exp.mkv")

    def __del__(self):
        self.video.release()

    # returns camera frames along with bounding boxes and predictions
    def get_frame(self):
        _, fr = self.video.read()
        gray_fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        faces = facec.detectMultiScale(gray_fr, 1.3, 5)

        for (x, y, w, h) in faces:
            fc = gray_fr[y:y+h, x:x+w]

            roi = cv2.resize(fc, (48, 48))
            pred = model.predict_emotion(roi[np.newaxis, :, :, np.newaxis])

            cv2.putText(fr, pred, (x, y), font, 1, (255, 255, 0), 2)
            cv2.rectangle(fr,(x,y),(x+w,y+h),(255,0,0),2)

        _, jpeg = cv2.imencode('.jpg', fr)
        return jpeg.tobytes()
