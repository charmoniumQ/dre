#!/usr/bin/env python3
from servo import ServoControl
from camera import CanvasApi, CameraApi
from face import FaceApi
import contextlib

do_servo = True
do_face = True

class Main(CameraApi, FaceApi, CanvasApi, ServoControl):
    def __init__(self):
        CameraApi.__init__(self)
        FaceApi.__init__(self)
        CanvasApi.__init__(self)
        if do_servo:
            ServoControl.__init__(self)

    def callback(self):
        if self.img_ready():
            surface, img_file = self.get_img()
            self.set_display(surface)
            self.draw_line((self.xmid_px, 0),
                        (self.xmid_px, self.height_px))
            if do_face:
                result = self.get_face(img_file)
                if result:
                    (mouth_x, mouth_y), depth = result
                    print ("Aim: ", (mouth_y - self.ymid_px) * self.deg_per_px_y)
                    if do_servo:
                        self.turn(-mouth_x + self.xmid_px)
                        # self.aim((mouth_y - self.ymid_px) * self.deg_per_px_y, depth)
                    self.draw_dot((mouth_x, mouth_y))
                    print(depth)
        else:
            print('image not ready')

    def close(self):
        CameraApi.close(self)
        CanvasApi.close(self)

if __name__ == '__main__':
    with contextlib.closing(Main()) as m:
        m.run()
