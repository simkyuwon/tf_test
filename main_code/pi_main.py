import cv2
import serial
import image_processing
from const_variables import const
import datetime
import capture

log_file = open(f'log.txt', 'w')


def print_log(text):
    print(text)
    log_file.write(f"{datetime.datetime.now().strftime('%H-%M-%S.%f')} / {text}\n")


def tx_data(ser, send_data):
    print_log(f'tx : {hex(send_data)}')
    send_data = int(send_data).to_bytes(1, 'big')
    ser.write(send_data)


def rx_data(ser):
    if ser.inWaiting() > 0:
        receive = ser.read()
        ser.flush()
        print_log(f'rx : {receive}')
        return receive
    else:
        return None


if __name__ == '__main__':
    ftp = capture.FtpClient(ip_address="192.168.0.4", user="simkyuwon", passwd="mil18-76061632")
    while True:
        try:
            cap = cv2.VideoCapture(0)  # 카메라 켜기  # 카메라 캡쳐 (사진만 가져옴)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, const.WIDTH_SIZE)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, const.HEIGHT_SIZE)
            cap.set(cv2.CAP_PROP_FPS, const.FPS)
            cap.set(cv2.CAP_PROP_AUTO_WB, False)
            break
        except ConnectionError:
            print('cannot load camera!')

    serial_port = serial.Serial('/dev/ttyS0', const.BPS, timeout=0.1)
    serial_port.flush()  # serial cls

    robot_state_controller = image_processing.RobotStateController()

    while True:
        if rx_data(serial_port) is not None:
            break
    tx_data(serial_port, const.SIGNAL_CHECK)
    print_log("통신 시작")

    frame = None
    while True:
        ret, frame = cap.read()
        if ret is False:
            continue

        serial_data = rx_data(serial_port)
        if serial_data is not None:
            serial_data = serial_data[0]
        else:
            continue

        if cv2.waitKey(10) == 27:
            break

        if serial_data == const.SIGNAL_IMAGE:
            ftp.store_image(frame)
            tx_data(serial_port, robot_state_controller.operation(cv2.GaussianBlur(frame, (3, 3), 0)))
        elif serial_data == const.SIGNAL_STATE:
            robot_state_controller.state_change()
        print_log(robot_state_controller)
    cap.release()
