import yaml
import cognitive_face
import numpy as np
import math
import gevent
gevent.monkey.patch_socket()


class FaceApi(object):
    def __init__(self):
        with open('credentials.yaml') as f:
            credentials = yaml.load(f)
        cognitive_face.Key.set(credentials['key'])
        cognitive_face.BaseUrl.set(credentials['base_url'])

    def get_face_async(self, img_file, state):
        return gevent.spawn(self.get_face_sync, img_file, state)

    def get_face_sync(self, img_file, state):
        face_list = cognitive_face.face.detect(img_file, face_id=False, landmarks=True)
        img_file.close()
        if len(face_list) > 1:
            print('Mulitple faces detected; using first')
        if face_list:
            upper_lip = face_list[0]['faceLandmarks']['upperLipTop']
            face = face_list[0]['faceRectangle']
            diagonal = np.sqrt(np.float64(face['width'])**2 +
                                 np.float64(face['height'])**2)
            face_size = np.float64(48) / np.float64('0.003725')
            return ((round(upper_lip['x']), round(upper_lip['y'])),
                    face_size / diagonal), state
