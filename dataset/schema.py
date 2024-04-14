from PIL import Image
from app.src.models.models import *
from fastapi import File, UploadFile




class Criminal():
    def __init__(self, name: str=None, age: int=None, gender: bool=None, description:str=None,image: str=None):
        self.name = name
        self.age=age
        self.gender = "남자" if gender else "여자"
        self.description=description
        self.image = image
        self.encoding=self.initialize_encoding(image)
    def initialize_encoding(self,image):
        img = Image.open(image)
        face_encoding = mtcnn(img).to(device)
        face_encoding = resnet(face_encoding).to(device)
        return face_encoding