import cv2
import serial
from detect_keypoint_lite import DetectKeypoint
import capture
import time


def tx_data(ser, send_data):
    for one_byte in send_data:
        ser.write(serial.to_bytes([one_byte]))


def rx_data(ser):
    if ser.inWaiting() > 0:
        return ser.readline()[:-1].decode('ascii')
    else:
        return None


if __name__ == '__main__':
    BPS = 4800

    serial_port = serial.Serial('/dev/ttyS0', BPS, timeout=0.01)
    serial_port.flush()  # serial cls

    tf_model = DetectKeypoint()

    while True:
        if rx_data(serial_port) is not None:
            break

    print("통신 시작\n")

    W_View_size = 320
    H_View_size = 240
    FPS = 80  # PI CAMERA: 320 x 240 = MAX 90

    while True:
        try:
            cap = cv2.VideoCapture(0)  # 카메라 켜기  # 카메라 캡쳐 (사진만 가져옴)

            cap.set(3, W_View_size)
            cap.set(4, H_View_size)
            cap.set(5, FPS)
            break
        except ConnectionError:
            print('cannot load camera!')

    ftp = capture.FtpClient(ip_address="192.168.0.2", user="simkyuwon", passwd="mil18-76061632")

    while cv2.waitKey(10) != 27:
        ret, frame = cap.read()  # 무한루프를 돌려서 사진을 동영상으로 변경   # ret은 true/false
        frame = cv2.GaussianBlur(frame, (3, 3), 0)

        if not ret:
            print('cannot read camera!')
            continue

        data = rx_data(serial_port)
        if data is not None:
            print(f"Return DATA : {data}")

        if data == "LS":
            print("store image")
            ftp.store_image(frame)
            cv2.imshow('frame', frame)
            
        #start = time.time()
        #point_list = tf_model.detect_keypoint(frame)
        #print(time.time() - start)
        
        '''dst = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if point_list is not None:
            image_label = point_list[0][1]
            keypoint = (0, 0)
            max_prediction = -1
            for point in point_list[1:]:
                (h, w), label, score = point
                if label == 1 and score > max_prediction:
                    max_prediction = score
                    keypoint = (w, h)
                if label == 0:
                    dst = cv2.circle(dst, (w, h), 3, (255, 0, 0), 2)
                elif label == 1:
                    dst = cv2.circle(dst, (w, h), 3, (0, 255, 0), 2)
                elif label == 2:
                    dst = cv2.circle(dst, (w, h), 3, (0, 0, 255), 2)
            print(image_label)
            dst = cv2.circle(dst, keypoint, 8, (255, 255, 255), 4)
        cv2.imshow('image', dst)'''
    
        #     print("\n********** 라인트레이싱 **********")
        #     print("Return DATA: " + data)
        #     mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)  # 노랑최소최대값을 이용해서 maskyellow값지정
        #     ftp.store_image(frame)
        #     time.sleep(1)
        #
        #     res_line = mode_linetracer(mask_yellow)
        #     TX_data_py2(serial_port, res_line)

    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    cap.release()
