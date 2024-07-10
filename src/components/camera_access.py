# Importing required libraries 
import sys
import cv2 as cv
import numpy as np

# Importing exceptions and logging 
from src.components.find_landmarks import GestureRecog
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

            if not isinstance(camera_path,int):
                logging.info("Camera path must be given as an integer")

            else:
                cam = cv.VideoCapture(camera_path)

                if not cam.isOpened():
                    logging.info("Could not access camera")

                else:
                    logging.info("Camera accessed successfully")
                    
                    recognizer = GestureRecog()
                    logging.info('Recognisor initialised')

                    while cam.isOpened():
                        
                        #Access the frame 
                        ret, frame = cam.read()

                        # Recognise the image 
                        image = cv.flip(frame,1) # Flipping so it is mirrored
                        d_image = np.copy(image) # Image to draw on
                        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

                        m_landmarks, m_gestures, m_handed = recognizer.hand_predict(image) 

                        for hand_landmark, gestures, handedness in zip(m_landmarks,
                                                                       m_gestures, 
                                                                       m_handed):
                            #Set the landmarks into an array
                            landmark_array, z_position = self.make_landmark_array(image, hand_landmark)

                            #Draw a bounding box around he hand
                            self.draw_bounding_box(d_image, landmark_array)

                            #Add the landmarks for the image
                            self.draw_fingers(d_image, landmark_array, z_position)

                            #Add text for the image
                            self.add_text(d_image, gestures[0], landmark_array, handedness[0])
                        
                        cv.imshow('Camera', d_image)
                        if cv.waitKey(1) & 0xFF == ord('q'):
                            logging.info("Closing camera")
                            break
                    
                    cam.release()
                    cv.destroyAllWindows()

        except CustomException as e:
            raise CustomException(e,sys)
    
    def make_landmark_array(self,image, landmarks):
        """
        Stores the landmark (x,y) values in an array, as well as the z coordinates

        Inputs:
            image(open_cv_numpy_array) -> The specfic frame from the webcam
            landmarks(GestureRecognition.hand_landmarks) -> An object storing the landmark positions
        
            Outputs:
                landmark_array(np.array[tuples]) -> An array of tuples storing (x,y) coordinates
                z_coordinates(List[Floats]) -> A list of z_coordinates for each landmark
        """

        H,W = image.shape[:2]
        landmark_array = np.empty((0, 2), np.int16) # Numpy array for tuples (x,y) for each landmark
        z_position = [] # List of z coordinates for each landmark


        # Exracting the (x,y) position for each landmark
        for landmark in landmarks:

            landmark_x = min(int(landmark.x*W),W-1) # When unnormalising the values, making sure it does not exceed image bounds
            landmark_y = min(int(landmark.y*H),H-1)

            landmark_point = [np.array((landmark_x,landmark_y))]
            landmark_array = np.append(landmark_array, landmark_point, axis=0)
            z_position.append(landmark.z)
    
        return landmark_array, z_position
    
    def draw_bounding_box(self, image, landmark_array):

        """
        This method draws a bounding box around the hand 

        Inputs:
            image(open_cv_numpy_array) -> The specfic frame from the webcam
            landmark_array(np.array[tuples]) -> An array of tuples storing (x,y) coordinates
        
            Ouputs:
                None
        
        """

        #Using OpenCV to find the coordinates of the bounding box 
        x, y, w, h = cv.boundingRect(landmark_array)

        #Drawing the bounding box onto the frame
        cv.rectangle(image, (x, y), (x+w, y+h),
                        (0, 0, 0), 2)
        
    
    def draw_fingers(self, image, landmark_array, z_position):

        """
        This method draws the landmarks and connects them via lines onto the image

        Inputs:
            image(open_cv_numpy_array) -> The specfic frame from the webcam
            landmark_array(np.array[tuples]) -> An array of tuples storing (x,y) coordinates
            z_coordinates(List[Floats]) -> A list of z_coordinates for each landmark

        Outputs:
            None
        
        """

        # Define bounds for the landmark sizes
        def_rad = 25 
        max_r = 5 # Max width of the squares 

        # Loop through each landmark draw onto image. Size is defined by the z_coordinate 
        for i, landmark in enumerate(landmark_array):
            current_r = min(max_r, int(z_position[i]*def_rad))
            cv.rectangle(image, (landmark[0]-current_r, landmark[1]-current_r),
                        (landmark[0]+current_r, landmark[1]+current_r), (0,0,0), -1)

        # Draw the lines connecting the landmarks, based on documentation

        #Thumb
        cv.line(image, landmark_array[0], landmark_array[1], (0,0,0),1)
        cv.line(image, landmark_array[1], landmark_array[2], (0,0,0),1)
        cv.line(image, landmark_array[2], landmark_array[3], (0,0,0),1)
        cv.line(image, landmark_array[3], landmark_array[4], (0,0,0),1)

        #pointer
        cv.line(image, landmark_array[0], landmark_array[5], (0,0,0),1)
        cv.line(image, landmark_array[5], landmark_array[6], (0,0,0),1)
        cv.line(image, landmark_array[6], landmark_array[7], (0,0,0),1)
        cv.line(image, landmark_array[7], landmark_array[8], (0,0,0),1)
        cv.line(image, landmark_array[5], landmark_array[9], (0,0,0),1)

        #middle
        cv.line(image, landmark_array[9], landmark_array[10], (0,0,0),1)
        cv.line(image, landmark_array[10], landmark_array[11], (0,0,0),1)
        cv.line(image, landmark_array[11], landmark_array[12], (0,0,0),1)
        cv.line(image, landmark_array[9], landmark_array[13], (0,0,0),1)

        #ring
        cv.line(image, landmark_array[13], landmark_array[14], (0,0,0),1)
        cv.line(image, landmark_array[14], landmark_array[15], (0,0,0),1)
        cv.line(image, landmark_array[15], landmark_array[16], (0,0,0),1)
        cv.line(image, landmark_array[13], landmark_array[17], (0,0,0),1)

        #pinkie
        cv.line(image, landmark_array[0], landmark_array[17], (0,0,0),1)
        cv.line(image, landmark_array[17], landmark_array[18], (0,0,0),1)
        cv.line(image, landmark_array[18], landmark_array[19], (0,0,0),1)
        cv.line(image, landmark_array[19], landmark_array[20], (0,0,0),1)

    def add_text(self, image, gesture, landmark_array, handedness):
        """
        This method adds the text from the predicted gestures and hand side

        Inputs:
            image(open_cv_numpy_array) -> The specfic frame from the webcam
            landmark_array(np.array[tuples]) -> An array of tuples storing (x,y) coordinates
            gestures(GestureRecog.gestures) -> Object storing the predicted gesture
            handedness(GestureRecog.handedness) -> Object sotring the predicted hand
        
        Output:
            None

        """

        # Text generation
        font = cv.FONT_HERSHEY_SIMPLEX
        category = gesture.category_name

        if handedness.category_name == 'Right': # To take into the account the flip of the image to begin with
            hand = 'Left'
        elif handedness.category_name == 'Left':
            hand = 'Right'
        
        text = hand + ' | ' + category # Text to be outputted 

        # Positon of text box   
        x, y, _, _ = cv.boundingRect(landmark_array)
        tx_offset = x
        ty_offset = y-5

        # Text Size 
        (t_w, t_h) = cv.getTextSize(text, font, fontScale=0.5, thickness=1)[0]
        
        # Background for the text - Offset it by a margin of 2 pixels
        box_coords = ((tx_offset - 2, ty_offset + 2), (tx_offset + t_w + 2, ty_offset - t_h - 2))
        cv.rectangle(image, box_coords[0], box_coords[1], (0,0,0), cv.FILLED) # 

        # Pace the text on top of background
        cv.putText(image, text, (tx_offset,ty_offset), font, 0.5, (255,255,255), lineType=cv.LINE_AA)

if __name__ == "__main__":

    camera = Camera()
    camera(1)