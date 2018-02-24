import math
import cv2


class CameraApi(object):
    def __init__(self):
        self.vc = cv2.VideoCapture(1)

    def init_size(self, frame):
        self.height_px = len(frame)
        self.width_px = len(frame[0])
        self.ymid_px = self.height_px // 2
        self.xmid_px = self.width_px // 2
        self.width_deg = math.atan((131 / 2) / 228)
        self.height_deg = math.atan((74.5 / 2) / 84)
        self.deg_per_px_x = self.width_px / self.width_deg
        self.deg_per_px_y = self.height_px / self.height_deg

    def get_img(self, return_file=False):
        if self.vc.isOpened():
            rval, frame = self.vc.read()
            if not rval:
                raise RuntimeError('Fail')
            else:
                self.init_size(frame)
                return frame, open(self.save_img(frame), 'rb')
        else:
            raise RuntimeError('Camera not opened')

    def save_img(self, frame):
        fname = 'img.png'
        cv2.imwrite(fname, frame)
        return fname

    def img_ready(self):
        return True

    def close(self):
        if self.vc is not None:
            self.vc.release()
            self.vc = None


class CanvasApi(object):
    def __init__(self):
        cv2.namedWindow("preview")
        self.frame = None

    def run(self):
        while True:
            self.callback()
            key = cv2.waitKey(20)
            if key == 27: # exit on ESC
                break

    def callback(self):
        print('over eyed me')

    def set_display(self, frame):
        self.frame = frame
        cv2.imshow("preview", frame)

    def draw_dot(self, pos):
        if self.frame is not None:
            cv2.circle(self.frame, pos, 10, (255, 0, 0), -1)
            cv2.imshow("preview", self.frame)

    def draw_line(self, pos1, pos2):
        if self.frame is not None:
            cv2.line(self.frame, pos1, pos2, (255, 0, 0), 2)
            cv2.imshow("preview", self.frame)

    def close(self):
        cv2.destroyWindow("preview")
