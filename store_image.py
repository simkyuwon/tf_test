import cv2
import os

path_dir = 'C:/Users/admin/Desktop/workspace/INIT/data/DATA_DIR'
file_list = os.scandir(path_dir)

min_height, min_width = 64, 88

for file in file_list:
    src = cv2.imread(f"{path_dir}/{file.name}", cv2.IMREAD_COLOR)
    src_height, src_width, src_channel = src.shape

    for i in range(0, 1):
        dst_height = int(min_height * pow(3/2, i))
        dst_width = int(min_width * pow(3/2, i))
        h_step = int(dst_height / 2)
        w_step = int(dst_width / 2)

        for h in range(11, src_height - dst_height, h_step):
            for w in range(11, src_width - dst_width, w_step):
                dst = src[h:h + dst_height, w:w + dst_width].copy()
                cv2.imwrite(f"{path_dir}/{dst_height}x{h}x{w}-{file.name}", dst)
