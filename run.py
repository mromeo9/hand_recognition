# Imports
import argparse
import cv2 as cv
from flask import Flask, render_template, Response

from src.components.camera_access import Camera
from src.components.models.sign_language_classifier.sign_language import SignLanguageClassifier
from src.components.find_landmarks import GestureRecog
from src.logger import logging
from src.exceptions import CustomException


app = Flask(__name__)

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--mode", type=int, default=0)
    parser.add_argument("-l", "--label", type=int)

    args = parser.parse_args()

    return args

def main():

    # Parser ang arguments
    parser = get_args()
    mode = parser.mode
    label = parser.label

    #Initialise the camera
    camera = Camera(camera_path=1, label = label, mode = mode)

    # Set up the models
    recognizer = GestureRecog()
    sign_language_classifier = SignLanguageClassifier()
    
    while camera.cam.isOpened():
        ret, frame = camera.get_frame(sign_language_classifier, recognizer)

        if not ret:
            break
        
        cv.imshow('Camera', frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    camera.cam.release()
    cv.destroyAllWindows()





@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def run():
    return Response(main, mimetype='multipart/x-mixed-replace: boundary=frame')

if __name__ == '__main__':
    #app.run(debug=True)
    main()

