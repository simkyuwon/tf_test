import tflite_runtime.interpreter as tflite
import numpy as np
import cv2
import pathlib


class DetectKeypoint:
    IMAGE_UNIT = ((64, 88), (96, 132), (144, 198), (216, 297))  # (height, width)
    IMAGE_HEIGHT, IMAGE_WIDTH = (240, 320)

    def __init__(self):
        model_path = "model.tflite"
        if not pathlib.Path.exists(pathlib.Path(model_path)):
            raise Exception("model not found")
        self.interpreter = tflite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def detect_keypoint(self, src_image):
        src_image = cv2.cvtColor(src_image, cv2.COLOR_RGB2BGR)
        image_array = np.asarray(src_image, dtype=np.float32)
        image_array = np.expand_dims(image_array, axis=0)
        return self.search(image_array, 3, (11, 11), -1)

    def search(self, image_array, size, point, label):
        height, width = point
        unit_height, unit_width = self.IMAGE_UNIT[size]

        if height + unit_height >= self.IMAGE_HEIGHT or width + unit_width >= self.IMAGE_WIDTH:
            return

        resize_image = np.resize(image_array[:, int(height):int(height + unit_height),
                                 int(width):int(width + unit_width)],
                                 (1, 64, 88, 3))
        self.interpreter.set_tensor(self.input_details[0]['index'], resize_image)
        self.interpreter.invoke()
        prediction = self.interpreter.get_tensor(self.output_details[0]['index'])
        prediction_label = np.argmax(prediction)
        prediction = np.max(prediction)

        ret_list = []
        if size == 3:
            label = prediction_label
            ret_list = [(point, prediction_label, prediction)]

        if size == 0:
            if prediction > 0.7:
                return [((int(height + unit_height / 2), int(width + unit_width / 2)), prediction_label, prediction)]
            else:
                return
        else:
            if prediction_label != 0:  # NOT FLOOR
                for h in range(2):
                    for w in range(2):
                        point_list = self.search(image_array, size - 1,
                                                 (height + (unit_height / 2) * h, width + (unit_width / 2) * w), label)
                        if point_list is not None:
                            ret_list = ret_list + point_list
                return ret_list
            else:
                return
