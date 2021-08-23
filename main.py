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

    if point_list is not None:
        image_label = point_list[0][1]
        keypoint = (0, 0)
        max_prediction = -1
        for point in point_list[1:]:
            (h, w), label, score = point
            if label != 2 and label != 3 and score > max_prediction:
                max_prediction = score
                keypoint = (w, h)
            if label == 0:
                dst = cv2.circle(dst, (w, h), 3, (255, 0, 0), 2)
            elif label == 1:
                dst = cv2.circle(dst, (w, h), 3, (0, 255, 0), 2)
            elif label == 3:
                dst = cv2.circle(dst, (w, h), 3, (0, 0, 255), 2)
            elif label == 4:
                dst = cv2.circle(dst, (w, h), 3, (0, 255, 255), 2)

        print(image_label)
        dst = cv2.circle(dst, keypoint, 8, (255, 255, 255), 4)
    cv2.imshow(f'image{i}', dst)

    # src = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
    # src_height, src_width, src_channel = src.shape
    #
    # for j in range(3, -1, -1):
    #     dst = cv2.cvtColor(src, cv2.COLOR_RGB2BGR)
    #
    #     dst_height = int(min_height * pow(3/2, j))
    #     dst_width = int(min_width * pow(3/2, j))
    #     h_step = int(dst_height / 2)
    #     w_step = int(dst_width / 2)
    #
    #     np_img = np.asarray(src)
    #     np_img = np.expand_dims(np_img, axis=0)
    #
    #     prediction_max = 0
    #     prediction_point = (0, 0)
    #
    #     range_height = src_height - dst_height
    #     range_width = src_width - dst_width
    #     for h in range(11, range_height, h_step):
    #         for w in range(11, range_width, w_step):
    #             prediction = model.predict(np_img[:, h:h + dst_height, w:w + dst_width])
    #
    #             prediction_label = np.argmax(prediction)
    #
    #             if image_label == -1:
    #                 image_label = prediction_label
    #
    #             if prediction_label == image_label and np.max(prediction) > prediction_max:
    #                 prediction_max = np.max(prediction)
    #                 prediction_point = (w + int(dst_width / 2), h + int(dst_height / 2))
    #
    #             if np.max(prediction) > 0.7:
    #                 if prediction_label == 0:
    #                     dst = cv2.circle(dst, (w + int(dst_width / 2), h + int(dst_height / 2)), 3, (255, 0, 0), 2)
    #                 elif prediction_label == 1:
    #                     dst = cv2.circle(dst, (w + int(dst_width / 2), h + int(dst_height / 2)), 3, (0, 255, 0), 2)
    #                 elif prediction_label == 3:
    #                     dst = cv2.circle(dst, (w + int(dst_width / 2), h + int(dst_height / 2)), 3, (0, 0, 255), 2)
    #                 elif prediction_label == 4:
    #                     dst = cv2.circle(dst, (w + int(dst_width / 2), h + int(dst_height / 2)), 3, (255, 255, 0), 2)
    #
    #     dst = cv2.circle(dst, prediction_point, 8, (255, 255, 255), 4)
    #
    #     cv2.imshow(f'image{i}{j}', dst)

cv2.waitKey(0)
cv2.destroyAllWindows()
