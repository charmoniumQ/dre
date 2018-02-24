#!/usr/bin/env python3
from servo import ServoControl
from camera import CanvasApi, CameraApi
from face import FaceApi


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
                self.turn(-mouth_x + self.xmid_px)
                self.aim((mouth_y - self.ymid_px) * self.deg_per_px_y, depth)
                self.draw_dot((mouth_x, mouth_y))
                self.draw_line((self.xmid_px, 0),
                               (self.xmid_px, self.height_px))
                print(depth)
        else:
            print('image not ready')

    def close(self):
        CameraApi.close(self)
        CanvasApi.close(self)

if __name__ == '__main__':
    with contextlib.closing(Main()) as m:
        m.run()
