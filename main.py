#!/usr/bin/env python3
import time
import contextlib
from servo import ServoControl
from camera import CanvasApi, CameraApi
from face import FaceApi

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
                (mouth_x, mouth_y), face_size = result
                max_x = len(surface[0])
                max_y = len(surface)
                mid_x = max_x // 2
                self.turn(-mouth_x + mid_x)
                self.aim(mouth_y)
                self.draw_dot((mouth_x, mouth_y))
                self.draw_line((mid_x, 0), (mid_x, max_y))
        else:
            print('image not ready')

    def close(self):
        CameraApi.close(self)
        CanvasApi.close(self)

with contextlib.closing(Main()) as m:
    m.run()
