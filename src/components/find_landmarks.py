import mediapipe as mp

class GestureRecog():

    def __init__(self):

        self.BaseOptions = mp.tasks.BaseOptions
        self.GestureRecognizer = mp.tasks.vision.GestureRecognizer
        self.GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
        self.GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
        self.VisionRunningMode = mp.tasks.vision.RunningMode

        self.options = self.GestureRecognizerOptions(
            base_options=self.BaseOptions(model_asset_path='/path/to/model.task'),
            running_mode=self.VisionRunningMode.LIVE_STREAM,
            result_callback=self.print_result)
    
    def print_result(result:GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
        print('gesture recognition result: {}'.format(result))

    def hand_predict(self, frame):

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        with self.GestureRecognizer.create_from_options(self.options) as recogniser:
            recogniser.recognize_async(mp_image)
