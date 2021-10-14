import cv2
import numpy as np
from const_variables import const


def calculate_angle(x_diff, y_diff):
    if x_diff == 0:
        return np.arctan(np.inf)
    else:
        return np.arctan(y_diff / x_diff)


def calculate_distance(point1, point2):
    return np.sum(np.square(np.array((point1[0], point1[1])) - np.array((point2[0], point2[1]))))


def detect_corner(line_list):
    if line_list is not None and len(line_list) >= 2:
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


def is_cross(line_list, corner_point):
    if (line_list is None) or (len(line_list) <= 1):
        return False

    for line in line_list:
        x_start, y_start, x_end, y_end, angle, x_pos = line
        if calculate_distance((x_start, y_start), corner_point) > 400 and \
                calculate_distance((x_end, y_end), corner_point) > 400:
            return True
    return False


class LineTracing:
    cross_kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

    def __init__(self):
        self.img_height = const.HEIGHT_SIZE
        self.img_width = const.WIDTH_SIZE

        self.prev_angle = np.pi / 2
        self.prev_x = const.WIDTH_SIZE / 2
        self.prev_motion = 0
        self.cross_check = 0

    def init(self):
        self.prev_angle = np.pi / 2
        self.prev_x = const.WIDTH_SIZE / 2
        self.prev_motion = 0
        self.cross_check = 0

    def find_main_line_index(self, line_list):
        if line_list is not None and len(line_list):
            line_array = np.asarray(line_list)[:, 4]
            line_array = abs(line_array - self.prev_angle)
            line_array = np.where(line_array >= np.pi / 2, abs(line_array - np.pi), line_array)
            if np.min(line_array) < np.pi / 4:
                return np.argmin(line_array)
        return None

    def select_line_motion(self, line_list):
        ret_value = const.MOTION_LINE_MOVE_FRONT
        line_index = self.find_main_line_index(line_list)
        if line_index is None:  # 라인 미검출
            if self.prev_motion == const.MOTION_LINE_MOVE_RIGHT:
                ret_value = const.MOTION_LINE_MOVE_LEFT
            elif self.prev_motion == const.MOTION_LINE_MOVE_LEFT:
                ret_value = const.MOTION_LINE_MOVE_RIGHT
            elif self.prev_motion == const.MOTION_LINE_TURN_RIGHT_SMALL:
                if self.prev_x < self.img_width / 2:
                    ret_value = const.MOTION_LINE_MOVE_LEFT
                else:
                    ret_value = const.MOTION_LINE_MOVE_RIGHT
            elif self.prev_motion == const.MOTION_LINE_TURN_LEFT_SMALL:
                if self.prev_x < self.img_width / 2:
                    ret_value = const.MOTION_LINE_MOVE_LEFT
                else:
                    ret_value = const.MOTION_LINE_MOVE_RIGHT
            else:
                ret_value = const.MOTION_LINE_LOST
        else:
            x_start, y_start, x_end, y_end, angle, x_pos = line_list[line_index]
            if -np.pi * 75 / 180 <= angle <= 0:
                ret_value = const.MOTION_LINE_TURN_RIGHT_SMALL
            elif 0 <= angle <= np.pi * 75 / 180:
                ret_value = const.MOTION_LINE_TURN_LEFT_SMALL
            elif x_pos < self.img_width * 0.35:
                ret_value = const.MOTION_LINE_MOVE_LEFT
            elif x_pos > self.img_width * 0.65:
                ret_value = const.MOTION_LINE_MOVE_RIGHT
            self.prev_angle, self.prev_x = angle, x_pos
        self.prev_motion = ret_value
        return ret_value

    def select_corner_motion(self, line_list):
        ret_value = self.select_line_motion(line_list)
        corner_point = detect_corner(line_list)

        if (corner_point is None) or is_cross(line_list, corner_point):
            self.cross_check = 0
        else:
            self.cross_check += 1

        if (not corner_point) or (self.cross_check <= 1):
            if ret_value == const.MOTION_LINE_LOST:
                ret_value = const.MOTION_LINE_STOP
        else:
            if ret_value == const.MOTION_LINE_TURN_RIGHT_SMALL or ret_value == const.MOTION_LINE_TURN_LEFT_SMALL:
                pass
            else:
                ret_value = const.MOTION_LINE_STOP
                x, y = corner_point
                if x < self.img_width * 0.35:
                    ret_value = const.MOTION_LINE_MOVE_LEFT
                elif x > self.img_width * 0.65:
                    ret_value = const.MOTION_LINE_MOVE_RIGHT
                elif y < self.img_height * 0.6:
                    ret_value = const.MOTION_LINE_MOVE_FRONT
        return ret_value

    def select_cross_motion(self, line_list):
        ret_value = const.MOTION_LINE_STOP
        corner_point = detect_corner(line_list)

        if (not corner_point) or (not is_cross(line_list, corner_point)):
            ret_value = self.select_line_motion(line_list)
            if ret_value == const.MOTION_LINE_LOST:
                ret_value = const.MOTION_LINE_STOP
        else:
            x, y = corner_point
            if x < self.img_width * 0.3:
                ret_value = const.MOTION_LINE_MOVE_LEFT
            elif x > self.img_width * 0.7:
                ret_value = const.MOTION_LINE_MOVE_RIGHT
            elif y < self.img_height * 0.4:
                ret_value = const.MOTION_LINE_MOVE_FRONT
        return ret_value

    def merge_line(self, line_list):
        ret_list = []
        line_list.sort()
        while len(line_list):
            x1_start, y1_start, x1_end, y1_end, angle1, __ = line_list[0]
            merge_list = [0]
            for index2, line2 in enumerate(line_list[1:], 1):
                x2_start, y2_start, x2_end, y2_end, angle2, __ = line2
                if abs(angle1 - angle2) < np.pi / 6:
                    if calculate_distance((x1_end, y1_end), (x2_start, y2_start)) < 500:
                        x1_end, y1_end = x2_end, y2_end
                        angle1 = calculate_angle(x1_end - x1_start, y1_end - y1_start)
                        merge_list.append(index2)
            if angle1 == 0:
                new_x_pos = np.inf
            else:
                new_x_pos = (self.img_height - y1_start) / np.tan(angle1) + x1_start
            ret_list.append([x1_start, y1_start, x1_end, y1_end, angle1, new_x_pos])
            merge_list.reverse()
            for index in merge_list:
                del line_list[index]
        return ret_list

    def detect_line(self, img_src):
        threshold_value, img_threshold = cv2.threshold(cv2.split(cv2.cvtColor(img_src, cv2.COLOR_BGR2HSV))[1],
                                                       0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        if threshold_value < 15:
            return None

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
            if len(pixel_list) > 300:
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
