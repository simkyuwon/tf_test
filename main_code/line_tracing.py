import cv2
import numpy as np
from const_variables import const


def calculate_angle(x_diff, y_diff):
    if x_diff == 0:
        return np.arctan(np.inf)
    else:
        return np.arctan(y_diff / x_diff)


def detect_corner(line_list):
    if len(line_list) >= 2:
        x1_start, y1_start, x1_end, y1_end, angle1, x1_pos = line_list[0]
        x2_start, y2_start, x2_end, y2_end, angle2, x2_pos = line_list[1]
        m1, m2 = np.tan(angle1), np.tan(angle2)
        arr1 = np.array([[m1, -1],
                         [m2, -1]])
        arr2 = np.array([m1 * x1_start - y1_start,
                         m2 * x2_start - y2_start])
        corner_x, corner_y = np.linalg.inv(arr1) @ arr2
        return corner_x, corner_y
    return None


class LineTracing:
    cross_kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

    def __init__(self, height=240, width=320):
        self.img_height = height
        self.img_width = width
        self.height_range = range(height)
        self.width_range = range(width)

        self.prev_angle = np.pi / 2
        self.prev_x = width / 2
        self.prev_motion = 0

    def find_main_line_index(self, line_list):
        if len(line_list) > 0:
            line_array = np.asarray(line_list)[:, 4]
            line_array = abs(line_array - self.prev_angle)
            line_array = np.where(line_array >= np.pi / 2, abs(line_array - np.pi), line_array)
            return np.argmin(line_array)
        return None

    def select_line_motion(self, line_list):
        ret_value = const.MOTION_LINE_MOVE_FRONT
        if len(line_list) == 0:  # 라인 미검출
            ret_value = const.MOTION_LINE_LOST
        else:
            line_index = self.find_main_line_index(line_list)
            x_start, y_start, x_end, y_end, angle, x_pos = line_list[line_index]
            if x_pos < self.img_width / 3:
                ret_value = const.MOTION_LINE_MOVE_LEFT
            elif x_pos > self.img_width * 2 / 3:
                ret_value = const.MOTION_LINE_MOVE_RIGHT
            elif -np.pi / 3 <= angle <= 0:
                ret_value = const.MOTION_LINE_TURN_RIGHT_SMALL
            elif 0 <= angle <= np.pi / 3:
                ret_value = const.MOTION_LINE_TURN_LEFT_SMALL
            self.prev_angle, self.prev_x = angle, x_pos
        self.prev_motion = ret_value
        return ret_value

    def select_corner_motion(self, line_list):
        ret_value = const.MOTION_LINE_STOP
        if len(line_list) == 0:
            ret_value = const.MOTION_LINE_LOST
        else:
            # line_index = self.find_main_line_index(line_list)
            # x_start, y_start, x_end, y_end, angle, x_pos = line_list[line_index]
            # if -np.pi / 3 <= angle <= 0:
            #     ret_value = const.MOTION_LINE_TURN_RIGHT_SMALL
            # elif 0 <= angle <= np.pi / 3:
            #     ret_value = const.MOTION_LINE_TURN_LEFT_SMALL
            # else:
            corner_point = detect_corner(line_list)
            if corner_point is None:
                ret_value = const.MOTION_LINE_LOST
            else:
                x, y = corner_point
                if x < self.img_width / 4:
                    ret_value = const.MOTION_LINE_MOVE_LEFT
                elif x > self.img_width * 3 / 4:
                    ret_value = const.MOTION_LINE_MOVE_RIGHT
                elif y < self.img_height / 4:
                    ret_value = const.MOTION_LINE_MOVE_FRONT
        return ret_value

    def merge_line(self, line_list):
        ret_list = []

        for index1, line1 in enumerate(line_list):
            x1_start, y1_start, x1_end, y1_end, angle1, __ = line1
            for index2, line2 in enumerate(line_list[index1 + 1:], index1 + 1):
                x2_start, y2_start, x2_end, y2_end, angle2, __ = line2
                if abs(angle1 - angle2) < np.pi / 6:
                    if np.sum(np.square(np.array((x1_end, y1_end)) - np.array((x2_start, y2_start)))) < 500:
                        x1_end, y1_end = x2_end, y2_end
                        line_list.pop(index2)
                    elif np.sum(np.square(np.array((x1_start, y1_start)) - np.array((x2_end, y2_end)))) < 500:
                        x1_start, y1_start = x2_start, y2_start
                        line_list.pop(index2)
            new_angle = calculate_angle(x1_end - x1_start, y1_end - y1_start)
            if new_angle == 0:
                new_x_pos = np.inf
            else:
                new_x_pos = (self.img_height - y1_start) / np.tan(new_angle) + x1_start
            ret_list.append([x1_start, y1_start, x1_end, y1_end, new_angle, new_x_pos])
        return ret_list

    def detect_line(self, img_src):
        img_threshold = cv2.threshold(cv2.split(cv2.cvtColor(img_src, cv2.COLOR_BGR2HSV))[1],
                                      0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        img_threshold = cv2.erode(img_threshold, self.cross_kernel, iterations=5)
        img_skeleton = np.zeros(img_threshold.shape, np.uint8)

        while True:
            eroded = cv2.erode(img_threshold, self.cross_kernel, borderType=cv2.BORDER_REPLICATE)
            subtracted = cv2.bitwise_xor(img_threshold, cv2.dilate(eroded, self.cross_kernel))
            img_skeleton = cv2.bitwise_or(img_skeleton, subtracted)
            if not cv2.countNonZero(img_threshold):
                break
            img_threshold = eroded.copy()

        img_skeleton = cv2.dilate(img_skeleton, self.cross_kernel, borderType=cv2.BORDER_CONSTANT, borderValue=0)

        corner_array = np.asarray(np.where(cv2.cornerHarris(img_skeleton, 3, 5, 0.1) > 0.5, 0, 255), dtype=np.uint8)
        corner_array = cv2.erode(corner_array, self.cross_kernel, iterations=3)
        img_skeleton = cv2.bitwise_and(img_skeleton, corner_array)

        img_labeling, stats = cv2.connectedComponentsWithStats(img_skeleton, connectivity=4)[1:3]

        line_list = []
        label_max = np.max(img_labeling)
        for label in range(1, label_max + 1):
            pixel_list = np.argwhere(img_labeling == label)
            if len(pixel_list) > 200:
                pixel_list = np.asarray(pixel_list, dtype=np.float64)
                x_array = np.reshape(pixel_list[:, 1], -1)
                y_array = np.reshape(pixel_list[:, 0], -1)
                x_array = np.vstack([x_array, np.ones(x_array.shape[0])]).T
                m, c = np.linalg.lstsq(x_array, y_array, rcond=-1)[0]  # y = mx + c

                if m == 0:
                    m = 0.0001

                if stats[label][2] > stats[label][3]:
                    x_start, x_end = stats[label][0], stats[label][0] + stats[label][2]
                    y_start, y_end = m * x_start + c, m * x_end + c
                else:
                    y_start, y_end = stats[label][1], stats[label][1] + stats[label][3]
                    x_start, x_end = (y_start - c) / m, (y_end - c) / m

                line_angle = calculate_angle(x_end - x_start, y_end - y_start)
                line_list.append([x_start, y_start, x_end, y_end, line_angle, 0])
        return self.merge_line(line_list)
