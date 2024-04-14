
from app.src.models.models import *
from app.src.middleware.settings import *
from app.src.models.database import *
from app.src.dataset.schema import *
from pydantic import parse_obj_as

def load_known_faces(criminals):


    known_face_encodings=[]

    for criminal in criminals:
        known_face_encodings.append(Criminal(name=criminal.name,age=criminal.age
                                             ,description=criminal.description,
                                             gender=criminal.gender,image=criminal.image))

    return known_face_encodings