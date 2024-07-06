# Importing required libraries 
import sys
import cv2 as cv

# Importing exceptions and logging 
from src.exceptions import CustomException
from src.logger import logging

class Camera():
    """
    Camera class to create an object to acces the camera
    """

    def __call__(self, camera_path: int = None):
        """
        On call the camera object will access the camera
        """
        try:
            logging.info("Trying to access the camera")

            if isinstance(camera_path,int):
                logging.info("Camera path must be given as an integer")

            else:
                cam = cv.VideoCapture(camera_path)

                if not cam.isOpened():
                    logging.info("Could not access camera")

                else:
                    logging.info("Camera accessed successfully")
                    
                    while cam.isOpened():
                        
                        #Access the frame 
                        ret, frame = cam.read()
                        cv.imshow('Camera', frame)

                        if cv.waitKey(1) & 0xFF == ord('q'):
                            logging.info("Closing camera")
                            break
                    
                    cam.release()
                    cv.destroyAllWindows()

        except CustomException as e:
            raise CustomException(e,sys)

if __name__ == "__main__":

    camera = Camera()
    camera(1)