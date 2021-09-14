import tflite_runtime.interpreter as tflite
import numpy as np
import cv2
import pathlib
from const_variables import const


class DirectionRecognition:
    def __init__(self):
        self.model_path = "model.tflite"
        if not pathlib.Path.exists(pathlib.Path(self.model_path)):
            raise Exception("model not found")
        self.interpreter = tflite.Interpreter(model_path=self.model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def predict(self, source_image):
        ret_value = const.MOTION_DIRECTION_UNKNOWN

        image_array = cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY)
        image_array = cv2.bitwise_not(image_array)
        image_array = np.asarray(image_array, dtype=np.float32)
        image_array = np.expand_dims(image_array, axis=2)
        image_array = np.expand_dims(image_array, axis=0)

        self.interpreter.set_tensor(self.input_details[0]['index'], image_array)
        self.interpreter.invoke()
        prediction = self.interpreter.get_tensor(self.output_details[0]['index'])
        prediction_label = np.argmax(prediction)

        if np.max(prediction) < 0.5:
            ret_value = const.MOTION_DIRECTION_UNKNOWN
        elif prediction_label == 0:
            ret_value = const.MOTION_DIRECTION_DOOR
        elif prediction_label == 1:
            ret_value = const.MOTION_DIRECTION_EAST
        elif prediction_label == 2:
            ret_value = const.MOTION_DIRECTION_NORTH
        elif prediction_label == 3:
            ret_value = const.MOTION_DIRECTION_SOUTH
        elif prediction_label == 4:
            ret_value = const.MOTION_DIRECTION_WEST

        return ret_value
