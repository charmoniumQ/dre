#!/usr/bin/env python3
import cognitive_face
import pygame, pygame.image
import cv2
import yaml
import time
import contextlib
from servo import ServoControl


@contextlib.contextmanager
def print_time(label):
    start = time.time()
    yield
    end = time.time()
    elapsed = end - start
    print('{elapsed: 2.4f}s: {label:}'.format(**locals()))

def print_time_f(func):
    def func_(*args, **kwargs):
        with print_time(func.__name__):
            return func(*args, **kwargs)
    return func_


class FaceApi(object):
    def __init__(self):
        with open('credentials.yaml') as f:
            credentials = yaml.load(f)
        cognitive_face.Key.set(credentials['key'])
        cognitive_face.BaseUrl.set(credentials['base_url'])

    def get_face(self, img_file):
        face_list = cognitive_face.face.detect(img_file, face_id=False, landmarks=True)
        img_file.close()
        if len(face_list) != 1:
            print('Mulitple faces detected; using first')
        if face_list:
            mouth = face_list[0]['faceLandmarks']['underLipTop']
            face = face_list[0]['faceRectangle']
            return ((round(mouth['x']), round(mouth['y'])), face['width'] * face['height'])


class CameraApi(object):
    def __init__(self):
        self.vc = cv2.VideoCapture(1)

    def get_img(self, return_file=False):
        if self.vc.isOpened():
            rval, frame = self.vc.read()
            if not rval:
                raise RuntimeError('Fail')
            else:
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


class Main(CameraApi, FaceApi, CanvasApi, ServoControl):
    def __init__(self):
        CameraApi.__init__(self)
        FaceApi.__init__(self)
        CanvasApi.__init__(self)
        ServoControl.__init__(self)

    def callback(self):
        if self.img_ready():
            surface, img_file = self.get_img()
            self.set_display(surface)
            result = self.get_face(img_file)
            if result:
                (mouth_x, mouth_y), depth = result
                max_x = len(surface[0])
                max_y = len(surface)
                mid_x = max_x // 2
                self.turn(-mouth_x + mid_x)
                self.draw_dot((mouth_x, mouth_y))
                self.draw_line((mid_x, 0), (mid_x, max_y))
        else:
            print('image not ready')

    def close(self):
        CameraApi.close(self)
        CanvasApi.close(self)

with contextlib.closing(Main()) as m:
    m.run()
