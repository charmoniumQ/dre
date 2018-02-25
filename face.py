import yaml
import cognitive_face
import numpy as np
import math
import gevent
import threading
from util import print_time


class FaceApi(object):
    def __init__(self):
        with open('credentials.yaml') as f:
            credentials = yaml.load(f)
        cognitive_face.Key.set(credentials['key'])
        cognitive_face.BaseUrl.set(credentials['base_url'])

    def get_face_async(self, img_file, state):
        result = {}
        event = threading.Event()
        threading.Thread(target=self.get_face_sync, args=(img_file, state, event))
        return (result, event)

    def get_face_sync(self, img_file, state, event):
        with print_time('cf sdk'):
            face_list = cognitive_face.face.detect(img_file, face_id=False, landmarks=True)
        gevent.sleep(0)
        with print_time('rest'):
            img_file.close()
            if face_list:
                if len(face_list) > 1:
                    print('Mulitple faces detected; using first')
                upper_lip = face_list[0]['faceLandmarks']['upperLipTop']
                face = face_list[0]['faceRectangle']
                diagonal = np.sqrt(np.float64(face['width'])**2 +
                                     np.float64(face['height'])**2)
                face_size = np.float64(48) / np.float64('0.003725')
                result['size'] = face_size / diagonal
                result['mouth'] = (round(upper_lip['x']), round(upper_lip['y']))
                result['state'] = state
            event.set()


def select(things):
    unfinished_things = []
    results = []
    for thing in things:
        


# def select(greenlets):
#     results = []
#     unfinished_greenlets = []
#     for greenlet in greenlets:
#         if greenlet.ready():
#             value = greenlet.value
#             if value is not None:
#                 results.append(value)
#         else:
#             unfinished_greenlets.append(greenlet)
#     return results, unfinished_greenlets
