
from app.src.models.models import *
from app.src.middleware.settings import *
from app.src.models.database import *
from app.src.dataset.schema import *
from pydantic import parse_obj_as

def load_known_faces():
    criminals = session.query(CriminalDao).all()


    known_face_encodings=[]




    for criminal in criminals:
        img = Image.open("resource/"+criminal.image_path)
        face_encoding = mtcnn(img)
        face_encoding = resnet(face_encoding.to(device))
        known_face_encodings.append(face_encoding)
    return known_face_encodings