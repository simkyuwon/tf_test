import tflite_runtime.interpreter as tflite
import numpy as np
import cv2
import pathlib
from const_variables import const


def check_section_color(source_image):
    hsv_image = cv2.cvtColor(source_image, cv2.COLOR_BGR2HSV)
    red_image = cv2.bitwise_or(cv2.inRange(hsv_image, const.RED_RANGE1[0], const.RED_RANGE1[1]),
                               cv2.inRange(hsv_image, const.RED_RANGE2[0], const.RED_RANGE2[1]))
    blue_image = cv2.inRange(hsv_image, const.BLUE_RANGE[0], const.BLUE_RANGE[1])

    if cv2.countNonZero(red_image) > cv2.countNonZero(blue_image):
        return "RED"
    else:
        return "BLUE"


class SectionRecognition:
    def __init__(self):
        self.model_path = "section_model.tflite"
        if not pathlib.Path.exists(pathlib.Path(self.model_path)):
            raise Exception("model not found")
        self.interpreter = tflite.Interpreter(model_path=self.model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def predict(self, source_image):
        rgb_image = cv2.cvtColor(source_image, cv2.COLOR_BGR2RGB)
        hsv_image = cv2.cvtColor(source_image[40:-40], cv2.COLOR_BGR2HSV)

        stats = cv2.connectedComponentsWithStats(cv2.threshold(
            np.asarray(cv2.split(hsv_image)[1]), 80, 255, cv2.THRESH_BINARY)[1])[2]

        stats_swap = stats.swapaxes(0, 1)
        stats = stats[np.where((stats_swap[4] > 200) & (stats_swap[4] < 2000))]

        max_prediction_value = 0.0
        ret_value = [np.zeros(5), ""]
        for stat in stats:
            x0, y0 = max(0, stat[0] - 4), max(0, stat[1] - 4 + 40)
            x1, y1 = min(const.WIDTH_SIZE, stat[0] + stat[2] + 4), min(const.HEIGHT_SIZE, stat[1] + stat[3] + 4 + 40)

            image_array = np.asarray(cv2.resize(rgb_image[y0:y1, x0:x1], (64, 64)), dtype=np.float32)
            image_array = np.expand_dims(image_array, axis=0)

            self.interpreter.set_tensor(self.input_details[0]['index'], image_array)
            self.interpreter.invoke()
            prediction = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
            if np.argmax(prediction) != 4 and np.max(prediction[:4]) > max_prediction_value:
                max_prediction_value = np.max(prediction[:4])
                ret_value = prediction, check_section_color(source_image[y0:y1, x0:x1])
        return ret_value

    def check_section_type(self, source_image):
        hsv_image = cv2.cvtColor(source_image[60:], cv2.COLOR_BGR2HSV)
        green_image = cv2.inRange(hsv_image, const.GREEN_RANGE[0], const.GREEN_RANGE[1])
        if cv2.countNonZero(green_image) > 2000:
            return const.MOTION_SECTION_SAFE
        else:
            return const.MOTION_SECTION_DANGER
