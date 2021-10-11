import cv2
import numpy as np
from const_variables import const


def find_milk_carton(source_image, color):
    binary_image = cv2.inRange(source_image, color[0], color[1])


class SafeSection:
    pass


class DangerSection:
    pass
