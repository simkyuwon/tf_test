import cv2
import ftplib
import datetime


class FtpClient:
    def __init__(self, ip_address="0.0.0.0", port=21, user="admin", passwd="0000"):
        try:
            self.ftp = ftplib.FTP()
            self.ftp.connect(ip_address, port)
            self.ftp.login(user, passwd)
        except ftplib.all_errors:
            print("ftp connect error")
            self.ftp = None

    def store_image(self, frame):
        if self.ftp is None:
            return
        cv2.imwrite("ftpImage.jpg", frame)
        img_file = open("ftpImage.jpg", "rb")
        self.ftp.storbinary(f"STOR {datetime.datetime.now().strftime('%Y%m%d-%H-%M-%S.%f')}.jpg", img_file)
        img_file.close()

