import cv2
import numpy as np


def merge_line(line_list):
    ret_list = []
    for index1, line1 in enumerate(line_list):
        (x1_start, y1_start), (x1_end, y1_end) = line1
        if y1_start == y1_end:
            gradient1 = np.inf
        else:
            gradient1 = (x1_start - x1_end) / (y1_start - y1_end)
        angle1 = np.arctan(gradient1)
        for index2, line2 in enumerate(line_list[index1 + 1:], index1 + 1):
            (x2_start, y2_start), (x2_end, y2_end) = line2
            if y2_start == y2_end:
                gradient2 = np.inf
            else:
                gradient2 = (x2_start - x2_end) / (y2_start - y2_end)
            angle2 = np.arctan(gradient2)
            if abs(angle1 - angle2) < np.pi / 9:
                if np.sum(np.square(np.array((x1_end, y1_end)) - np.array((x2_start, y2_start)))) < 500:
                    x1_end, y1_end = x2_end, y2_end
                    line_list.pop(index2)
                elif np.sum(np.square(np.array((x1_start, y1_start)) - np.array((x2_end, y2_end)))) < 500:
                    x1_start, y1_start = x2_start, y2_start
                    line_list.pop(index2)
        ret_list.append([(x1_start, y1_start), (x1_end, y1_end)])
    return ret_list


class DetectLine:
    cross_kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

    def __init__(self, height=240, width=320):
        self.img_height = height
        self.img_width = width

        self.height_range = range(height)
        self.width_range = range(width)

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

                if stats[label][2] > stats[label][3]:
                    x_start, x_end = stats[label][0], stats[label][0] + stats[label][2]
                    y_start, y_end = int(m * x_start + c), int(m * x_end + c)
                else:
                    y_start, y_end = stats[label][1], stats[label][1] + stats[label][3]
                    x_start, x_end = int((y_start - c) / m), int((y_end - c) / m)

                line_list.append([(int(x_start), int(y_start)), (int(x_end), int(y_end))])
        return merge_line(line_list)