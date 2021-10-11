import cv2
import numpy as np
from const_variables import const


def find_largest_contour(contours):
    largest_contour_index = -1
    largest_contour_area = 0

    for index, contour in enumerate(contours):
        contour_area = cv2.contourArea(contour)
        if contour_area > largest_contour_area:
            largest_contour_area = contour_area
            largest_contour_index = index
    if largest_contour_index != -1:
        return contours[largest_contour_index]
    else:
        return None


class ArrowRecognition:
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    def arrow_recognition(self, source_image):
        threshold_image = cv2.threshold(cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY),
                                        50, 255, cv2.THRESH_BINARY_INV)[1]
        threshold_image = cv2.morphologyEx(threshold_image, cv2.MORPH_CLOSE, self.rect_kernel)

        contour = find_largest_contour(cv2.findContours(threshold_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0])
        if contour is None:  # contour not found
            return const.MOTION_ARROW_UNKNOWN

        convex_hull = cv2.convexHull(contour, returnPoints=False)
        defects = cv2.convexityDefects(contour, convex_hull)
        start_index, end_index, farthest_index, farthest_length = defects[np.argmax(defects[:, :, 3], axis=0)[0], 0]
        start_point, end_point, farthest_point = contour[start_index][0], contour[end_index][0], contour[farthest_index][0]
        center_point = (start_point[0] + end_point[0]) // 2, (start_point[1] + end_point[1]) // 2
        if farthest_length < 1000:
            return const.MOTION_ARROW_UNKNOWN
        elif center_point[0] > farthest_point[0]:
            return const.MOTION_ARROW_LEFT
        else:
            return const.MOTION_ARROW_RIGHT

