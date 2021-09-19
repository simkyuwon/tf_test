import tensorflow as tf
from detect_keypoint import DetectKeypoint
import cv2
import time

min_height, min_width = 64, 88

tf_model = DetectKeypoint()

for i in range(4):
    src = cv2.imread(f"image{i}.jpg", cv2.IMREAD_COLOR)
    dst = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)

    start = time.time()
    point_list = tf_model.detect_keypoint(src)
    print(time.time() - start)

    image_label = point_list[0][1]
    if len(point_list) >= 2:
        if point_list[1] is not None:
            (h, w), label, score = point_list[1]
            if label == 0:
                dst = cv2.rectangle(dst, (w, h), (w + 88, h + 64), (255, 0, 0), 2)
            elif label == 1:
                dst = cv2.rectangle(dst, (w, h), (w + 88, h + 64), (0, 255, 0), 2)
            elif label == 3:
                dst = cv2.rectangle(dst, (w, h), (w + 88, h + 64), (0, 0, 255), 2)
            elif label == 4:
                dst = cv2.rectangle(dst, (w, h), (w + 88, h + 64), (0, 255, 255), 2)
    print(image_label)
    cv2.imshow(f'image{i}', dst)

cv2.waitKey(0)
cv2.destroyAllWindows()
