import cv2
import numpy as np


class DetectLine:
    cross_kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

    def detect_line(self, img_src):
        line_list = []
        img_hsv = cv2.cvtColor(img_src, cv2.COLOR_BGR2HSV)
        hsv_planes = cv2.split(img_hsv)
        img_threshold = cv2.threshold(hsv_planes[1], 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        img_threshold = cv2.morphologyEx(img_threshold, cv2.MORPH_OPEN, self.cross_kernel, iterations=2)
        img_skeleton = np.zeros(img_threshold.shape, np.uint8)

        while True:
            eroded = cv2.erode(img_threshold, self.cross_kernel, borderType=cv2.BORDER_ISOLATED)
            subtracted = cv2.subtract(img_threshold, cv2.dilate(eroded, self.cross_kernel, borderType=cv2.BORDER_ISOLATED))
            img_skeleton = cv2.bitwise_or(img_skeleton, subtracted)
            if not cv2.countNonZero(img_threshold):
                break
            img_threshold = eroded.copy()

        img_skeleton[0, :] = 0
        img_skeleton[-1, :] = 0
        img_skeleton[:, 0] = 0
        img_skeleton[:, -1] = 0

        img_skeleton = cv2.dilate(img_skeleton, self.cross_kernel, borderType=cv2.BORDER_ISOLATED)
        img_labeling, stats = cv2.connectedComponentsWithStats(img_skeleton, connectivity=8)[1:3]

        enum_stats = enumerate(stats[1:], start=1)
        height_range, width_range = range(img_labeling.shape[0]), range(img_labeling.shape[1])

        for (label, stat) in enum_stats:
            temp_list = np.empty((stat[4], 2), dtype=np.float32)
            count = 0
            for y in height_range:
                for x in width_range:
                    if img_labeling[y][x] == label:
                        temp_list[count] = [x, y]
                        count = count + 1
            if temp_list.shape[0] > 200:
                x_array = temp_list[:, 0:1]
                x_array = np.reshape(x_array, -1)
                y_array = temp_list[:, 1:2]
                y_array = np.reshape(y_array, -1)
                x_array = np.vstack([x_array, np.ones(x_array.shape[0])]).T
                m, c = np.linalg.lstsq(x_array, y_array, rcond=-1)[0]  # y = mx + c

                x_start, x_end = stat[0], stat[0] + stat[2]
                y_start, y_end = int(m * x_start + c), int(m * x_end + c)
                x_start, x_end = int(x_start), int(x_end)

                line_list.append([(x_start, y_start), (x_end, y_end)])

        return line_list
