#!/usr/bin/env python3
import cognitive_face
import pygame.camera
import pygame.image
import yaml


class CognitiveFaceWrapper(object):
    def __init__(self):
        with open('credentials.yaml') as f:
            credentials = yaml.load(f)
        cognitive_face.Key.set(credentials['key'])
        cognitive_face.BaseUrl.set(credentials['base_url'])
    
    def process_img(self):
        result = cognitive_face.face.detect(img_url)


class PygameWrapper(object):
    def __init__(self):
        print("hi")
        pygame.camera.init()
        self.cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
        self.cam.start()
        #cam.set_controls(hflip=True, vflip=False)
        print(camera.get_controls())


    def get_img(self):
        if self.cam is not None:
            img = self.cam.get_image()
            pygame.image.save(img, "photo.bmp")
        else:
            raise RuntimeError("Camera not initialized")

    def close(self):
        if self.cam is not None:
            self.cam.stop()
            self.cam = None
        pygame.camera.quit()
    

class Main(PygameWrapper, CognitiveFaceWrapper):
    pass


Main()
