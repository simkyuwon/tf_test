import tflite_runtime.interpreter as tflite
import numpy as np
import cv2
import pathlib


class SectionRecognition:
    red_range1 = [(0, 100, 50), (20, 255, 255)]
    red_range2 = [(160, 100, 50), (180, 255, 255)]
    blue_range = [(100, 100, 50), (120, 255, 255)]

    def __init__(self):
        self.model_path = "section_model.tflite"
        if not pathlib.Path.exists(pathlib.Path(self.model_path)):
            raise Exception("model not found")
        self.interpreter = tflite.Interpreter(model_path=self.model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def predict(self, source_image):
        hsv_image = cv2.cvtColor(source_image[40:-40], cv2.COLOR_BGR2HSV)
        h_array, s_array, __ = np.asarray(cv2.split(hsv_image))
        s_array[np.where((50 < h_array) & (h_array < 80))] = 0

        image_array = np.asarray(s_array, dtype=np.float32)
        image_array = np.expand_dims(image_array, axis=2)
        image_array = np.expand_dims(image_array, axis=0)

        self.interpreter.set_tensor(self.input_details[0]['index'], image_array)
        self.interpreter.invoke()
        return self.interpreter.get_tensor(self.output_details[0]['index'])[0]

    def check_section_color(self, source_image):
        hsv_image = cv2.cvtColor(source_image[50:-40], cv2.COLOR_BGR2HSV)
        red_image = cv2.bitwise_or(cv2.inRange(hsv_image, self.red_range1[0], self.red_range1[1]),
                                   cv2.inRange(hsv_image, self.red_range2[0], self.red_range2[1]))
        blue_image = cv2.inRange(hsv_image, self.blue_range[0], self.blue_range[1])

        __, labeling_array, labeling_stats, __ = cv2.connectedComponentsWithStats(cv2.bitwise_or(red_image, blue_image))
        labeling_stats_swap = labeling_stats.swapaxes(0, 1)
        labeling_stats = labeling_stats[np.where(labeling_stats_swap[2] * labeling_stats_swap[3] > 500)]

        if len(labeling_stats) > 1:
            roi_x, roi_y, roi_w, roi_h = labeling_stats[1][:4]
            roi_image = hsv_image[roi_y:roi_y + roi_h, roi_x:roi_x+roi_w]

            red_image = cv2.bitwise_or(cv2.inRange(roi_image, self.red_range1[0], self.red_range1[1]),
                                       cv2.inRange(roi_image, self.red_range2[0], self.red_range2[1]))
            blue_image = cv2.inRange(roi_image, self.blue_range[0], self.blue_range[1])
            if cv2.countNonZero(red_image) > cv2.countNonZero(blue_image):
                return "RED"
            else:
                return "BLUE"
        return "NOT FOUND"
