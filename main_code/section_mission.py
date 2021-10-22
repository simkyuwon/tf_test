import cv2
import numpy as np
from const_variables import const


def find_milk_carton(hsv_image, milk_carton_color):
    if milk_carton_color == "RED":
        milk_carton_image = cv2.bitwise_or(cv2.inRange(hsv_image, const.RED_RANGE1[0], const.RED_RANGE1[1]),
                                           cv2.inRange(hsv_image, const.RED_RANGE2[0], const.RED_RANGE2[1]))
    else:
        milk_carton_image = cv2.inRange(hsv_image, const.BLUE_RANGE[0], const.BLUE_RANGE[1])
    stats = cv2.connectedComponentsWithStats(milk_carton_image)[2]
    if len(stats) < 2:
        return None

    index = np.argmax(stats[1:].swapaxes(0, 1)[4]) + 1
    if stats[index][4] < 300:
        return None

    return stats[index]


def in_section(hsv_image):
    return cv2.countNonZero(cv2.inRange(hsv_image, const.WHITE_RANGE[0], const.WHITE_RANGE[1])) < 500


class SectionFind:
    def __init__(self, section_type):
        self.section_type = section_type
        self.section_color = ""

    def set_section_color(self, color):
        self.section_color = color

    def find_milk_carton(self, source_image):
        hsv_image = cv2.cvtColor(source_image[40:], cv2.COLOR_BGR2HSV)
        stat = find_milk_carton(hsv_image, self.section_color)

        if stat is None:
            return const.MOTION_MILK_NOT_FOUND

        point1 = (np.max([0, stat[0] - 10]), np.max([0, stat[1] - 10]))
        point2 = (np.min([const.WIDTH_SIZE, stat[0] + stat[2] + 10]),
                  np.min([const.HEIGHT_SIZE - 40, stat[1] + stat[3] + 10]))

        if in_section(hsv_image[point1[1]:point2[1], point1[0]:point2[0]]):
            return const.MOTION_MILK_FOUND if self.section_type == "DANGER" else const.MOTION_MILK_NOT_FOUND
        else:
            return const.MOTION_MILK_FOUND if self.section_type == "SAFE" else const.MOTION_MILK_NOT_FOUND


class SectionCatch:
    def __init__(self, section_type):
        self.section_type = section_type
        self.section_color = ""

    def set_section_color(self, color):
        self.section_color = color

    def select_motion(self, source_image):
        hsv_image = cv2.cvtColor(source_image, cv2.COLOR_BGR2HSV)
        stat = find_milk_carton(hsv_image, self.section_color)

        if stat is None:
            return const.MOTION_MILK_NOT_FOUND

        center_x, center_y = stat[0] + stat[2] / 2, stat[1] + stat[3] / 2

        if center_x < const.WIDTH_SIZE * 0.4:
            return const.MOTION_MILK_MOVE_LEFT
        elif center_x > const.WIDTH_SIZE * 0.6:
            return const.MOTION_MILK_MOVE_RIGHT
        elif center_y > const.HEIGHT_SIZE * 0.5:
            return const.MOTION_MILK_NOT_FOUND
        else:
            return const.MOTION_MILK_MOVE_FRONT


class SectionPut:
    def __init__(self, section_type):
        self.section_type = section_type

    def check_ground(self, source_image):
        hsv_image = cv2.cvtColor(source_image, cv2.COLOR_BGR2HSV)
        return const.MOTION_MILK_IN_SECTION if in_section(hsv_image[80:-80, 80:-80]) else const.MOTION_MILK_OUT_SECTION

