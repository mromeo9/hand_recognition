import mediapipe as mp
from dataclasses import dataclass

@dataclass
class GestureConfig:
    path_to_model = 'src/components/models/gesture_recognizer.task'

class GestureRecog():

    def __init__(self):
        # Set model path
        self.model_config = GestureConfig()

        #transform data
        with open(self.model_config.path_to_model,'rb') as file:
            self.model_data = file.read()

        # Setting the options and for the gesture recognisor
        self.BaseOptions = mp.tasks.BaseOptions
        self.GestureRecognizer = mp.tasks.vision.GestureRecognizer
        self.GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
        self.VisionRunningMode = mp.tasks.vision.RunningMode

        self.options = self.GestureRecognizerOptions(
            base_options=self.BaseOptions(model_asset_buffer=self.model_data),
            running_mode=self.VisionRunningMode.IMAGE,
            num_hands = 2)
        
        self.recognizer = self.GestureRecognizer.create_from_options(self.options)
        
    def hand_predict(self, frame):
         
        # Convert to Media Pipe image 
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        #Find the results
        gesture_recognition_result = self.recognizer.recognize(mp_image)

        #Extract the landmarks, gesture and hand
        multi_hand_landmarks = gesture_recognition_result.hand_landmarks
        multi_gestures = gesture_recognition_result.gestures
        multi_handedness = gesture_recognition_result.handedness

        return multi_hand_landmarks, multi_gestures, multi_handedness