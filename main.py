#!/usr/bin/env python3
import cognitive_face
import pygame, pygame.image
import cv2
import yaml

import time
import contextlib

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

    @print_time_f
    def get_face(self, img_file):
        face_list = cognitive_face.face.detect(img_file, face_id=False, landmarks=True)
        img_file.close()
        if len(face_list) != 1:
            print('Mulitple faces detected; using first')
        if face_list:
            mouth = face_list[0]['faceLandmarks']['underLipTop']
            face = face_list[0]['faceRectangle']
            return ((mouth['x'], mouth['y']), face['width'] * face['height'])


class CameraApi(object):
    def __init__(self):
        pygame.camera.init()
        cam_list = pygame.camera.list_cameras()
        if len(cam_list) != 1:
            print('Mulitple cameras detected; using last')
        self.cam = pygame.camera.Camera(pygame.camera.list_cameras()[-1])
        #self.cam.set_controls(hflip=True, vflip=False)
        self.cam.start()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @print_time_f
    def get_img(self, return_file=False):
        if self.cam is not None:
            img = self.cam.get_image()
            pygame.image.save(img, 'img.png')
            return open('img.png', 'rb'), img
        else:
            raise RuntimeError('Camera not initialized')

    def img_ready(self):
        return self.cam.query_image()

    def get_size(self):
        return self.cam.get_size()

    def close(self):
        if self.cam is not None:
            self.cam.stop()
            self.cam = None
        pygame.camera.quit()


class CanvasApi(object):
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode(self.get_size())

    def run(self):
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            self.callback()
            pygame.display.flip()

    def callback(self):
        print('over eyed me')

    def set_display(self, surface):
        self.display.blit(surface, (0, 0))

    def draw_dot(self, pos):
        red = (255,   0,   0)
        pygame.draw.circle(self.display, red, (int(pos[0]), int(pos[1])), 10, 0)

class Main(CameraApi, FaceApi, CanvasApi):
    def __init__(self):
        CameraApi.__init__(self)
        FaceApi.__init__(self)
        CanvasApi.__init__(self)

    def callback(self):
        print('img not ready')
        if self.img_ready():
            img_file, surface = self.get_img()
            self.set_display(surface)
            result = self.get_face(img_file)
            if result:
                mouth, depth = result
                self.draw_dot(mouth)


with Main() as m:
    m.run()
