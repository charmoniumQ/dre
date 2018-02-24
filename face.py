import yaml
import cognitive_face


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
