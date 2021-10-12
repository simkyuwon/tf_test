import cv2
import numpy as np
from const_variables import const


def find_milk_carton(source_image, section, milk_carton_color):
    print(f'section type : {section}, section color : {milk_carton_color}')
    hsv_image = cv2.cvtColor(source_image[40:], cv2.COLOR_BGR2HSV)
    if milk_carton_color == "RED":
        milk_carton_image = cv2.bitwise_or(cv2.inRange(hsv_image, const.RED_RANGE1[0], const.RED_RANGE1[1]),
                                           cv2.inRange(hsv_image, const.RED_RANGE2[0], const.RED_RANGE2[1]))
    else:
        milk_carton_image = cv2.inRange(hsv_image, const.BLUE_RANGE[0], const.BLUE_RANGE[1])

    stats = cv2.connectedComponentsWithStats(milk_carton_image)[2]

    if len(stats) < 2:
        return const.MOTION_MILK_NOT_FOUND

    index = np.argmax(stats[1:].swapaxes(0, 1)[4]) + 1
    if stats[index][4] < 300:
        return const.MOTION_MILK_NOT_FOUND

    point1 = (np.max([0, stats[index][0] - 10]), np.max([0, stats[index][1] - 10]))
    point2 = (np.min([320, stats[index][0] + stats[index][2] + 10]),
              np.min([240, stats[index][1] + stats[index][3] + 10]))

    ground_pixels_count = cv2.countNonZero(cv2.inRange(hsv_image[point1[1]:point2[1], point1[0]:point2[0]],
                                                       const.WHITE_RANGE[0], const.WHITE_RANGE[1]))

    if ground_pixels_count > 500:
        return const.MOTION_MILK_FOUND if section == "SAFE" else const.MOTION_MILK_NOT_FOUND
    else:
        return const.MOTION_MILK_FOUND if section == "DANGER" else const.MOTION_MILK_NOT_FOUND


class SectionFind:
    def __init__(self, section_type):
        self.section_type = section_type
        self.section_color = ""

    def set_section_color(self, color):
        self.section_color = color

    def find_milk_carton(self, source_image):
        return find_milk_carton(source_image, self.section_type, self.section_color)


class SectionCatch:
    pass


class SectionDrop:
    pass


class SectionComeback:
    pass
