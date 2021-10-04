import tflite_runtime.interpreter as tflite
import numpy as np
import cv2
import pathlib


class DirectionRecognition:
    def __init__(self):
        self.model_path = "direction_model.tflite"
        if not pathlib.Path.exists(pathlib.Path(self.model_path)):
            raise Exception("model not found")
        self.interpreter = tflite.Interpreter(model_path=self.model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def predict(self, source_image):
        image_array = cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY)
        image_array = np.asarray(image_array, dtype=np.float32)
        image_array = np.expand_dims(image_array, axis=2)
        image_array = np.expand_dims(image_array, axis=0)

        self.interpreter.set_tensor(self.input_details[0]['index'], image_array)
        self.interpreter.invoke()
        return self.interpreter.get_tensor(self.output_details[0]['index'])[0]
