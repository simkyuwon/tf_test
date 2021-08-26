from re import search

import tensorflow as tf
import numpy as np
import cv2
import pathlib


class DetectKeypoint:
    IMAGE_UNIT = ((64, 88), (96, 132), (144, 198), (216, 297))  # (height, width)
    IMAGE_HEIGHT, IMAGE_WIDTH = (240, 320)

    def __init__(self):
        model_path = "saved_model/model"
        if not pathlib.Path.exists(pathlib.Path(model_path)):
            raise Exception("model not found")
        self.model = tf.keras.models.load_model(model_path)

    def detect_keypoint(self, src_image):
        src_image = cv2.cvtColor(src_image, cv2.COLOR_RGB2BGR)
        image_array = np.asarray(src_image)
        image_array = np.expand_dims(image_array, axis=0)

        unit_height, unit_width = self.IMAGE_UNIT[3]

        prediction = np.array([self.model.predict(image_array[:, 0:unit_height, 0:unit_width])[0],
                               self.model.predict(image_array[:, 0:unit_height, -unit_width:])[0],
                               self.model.predict(image_array[:, -unit_height:, 0:unit_width])[0],
                               self.model.predict(image_array[:, -unit_height:, -unit_width:])[0]])

        # print(prediction)
        # print("max")
        # print(np.max(prediction[:, 0:2]))
        if np.max(prediction[:, 0:2]) > 0.7:
            index = np.argmax(prediction[:, 0:2])
            prediction_label = int(index % 2)
            index = int(index / 2)
        else:
            index = np.argmax(prediction)
            prediction_label = int(index % 5)

        ret_list = [((0, 0), prediction_label, np.max(prediction))]

        if prediction_label <= 1:  # CORNER or CROSS
            start_point = [(0, 0), (0, self.IMAGE_WIDTH - unit_width - 1), (self.IMAGE_HEIGHT - unit_height - 1, 0),
                           (self.IMAGE_HEIGHT - unit_height - 1, self.IMAGE_WIDTH - unit_width - 1)]
            ret_list = ret_list + self.search(image_array, 2, start_point[index])
        return ret_list

    def search(self, image_array, size, point):
        origin_height, origin_width = point
        unit_height, unit_width = self.IMAGE_UNIT[size]

        prediction = np.zeros(shape=(16, 5))
        height_step, width_step = int(unit_height / 3), int(unit_width / 3)
        prediction_index = 0
        for height in range(origin_height - height_step, origin_height + height_step * 3, height_step):
            for width in range(origin_width - width_step, origin_width + width_step * 3, width_step):
                if height >= 0 and width >= 0 \
                        and height + unit_height < self.IMAGE_HEIGHT and width + unit_width < self.IMAGE_WIDTH:
                    prediction[prediction_index] = self.model.predict(image_array[:,
                                                                      height:height + unit_height,
                                                                      width:width + unit_width])[0]
                prediction_index = prediction_index + 1

        index_array = np.argmax(prediction, axis=0)[:2]
        if prediction[index_array[0]][0] > prediction[index_array[1]][1]:
            label = 0
        else:
            label = 1

        if prediction[index_array[label]][label] < 0.5:
            return [None]
        # np.set_printoptions(precision=3, suppress=True)
        # print("prediction")
        # print(prediction)
        # print("label")
        # print(label)
        index = index_array[label]
        h = int(index / 4) - 1
        w = int(index % 4) - 1
        next_point = (int(origin_height + (unit_height / 3) * h), int(origin_width + (unit_width / 3) * w))
        if size == 0:
            return [(next_point, label, prediction[index][label])]
        else:
            return self.search(image_array, size - 1, next_point)
