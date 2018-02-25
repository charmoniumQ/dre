#!/usr/bin/env python3
from servo import ServoControl
from camera import CanvasApi, CameraApi
from face import FaceApi
from util import print_time
import contextlib

do_face = True
do_shoot = True
do_servo = True
first = True

class Main(CameraApi, FaceApi, CanvasApi, ServoControl):
    def __init__(self):
        CameraApi.__init__(self)
        FaceApi.__init__(self)
        CanvasApi.__init__(self)
        if do_servo:
            ServoControl.__init__(self)
        self.results = []

    def callback(self):
        if self.img_ready():
            with print_time('get img'):
                surface, img_file = self.get_img()
            with print_time('draw img'):
                self.set_display(surface)
                self.draw_line((self.xmid_px, 0),
                               (self.xmid_px, self.height_px))
            if do_face:
                with print_time('get face'):
                    self.results.append(self.get_face_async(img_file))

                if result:
                    (mouth_x, mouth_y), depth = result

                    global first
                    if first:
                        print(f'Field of view: {self.width_px}x{self.height_px} px')
                        print(f'Field of view: {self.width_deg:.0f}x{self.height_deg:.0f} deg')
                        print(f'degrees: {self.deg_per_px_x:.3f} {self.deg_per_px_y:.3f}')
                        first = False

                    self.draw_dot((mouth_x, mouth_y))
                    with print_time('do servo'):
                        altitude = (self.ymid_px - mouth_y) * self.deg_per_px_y
                        if do_servo:
                            self.turn(self.xmid_px - mouth_x)
                            self.aim(altitude, depth)
                            self.have_target()
                            if do_shoot:
                                self.maybe_fire()
                else:
                    self.cancel_target()
        else:
            print('image not ready')

    def close(self):
        CameraApi.close(self)
        CanvasApi.close(self)

if __name__ == '__main__':
    with contextlib.closing(Main()) as m:
        m.run()
