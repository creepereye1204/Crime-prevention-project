from PIL import Image
from app.src.models.models import *
from app.src.middleware.settings import *

def load_known_faces(person_images):
    known_face_encodings=[]
    for person_image in person_images:
        img = Image.open("resource/"+person_image)
        face_encoding = mtcnn(img)
        face_encoding = resnet(face_encoding.to(device))
        known_face_encodings.append(face_encoding)
    return known_face_encodings