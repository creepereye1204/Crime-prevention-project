from PIL import Image
from app.src.models.models import *
from fastapi import File, UploadFile




class Criminal():
    def __init__(self, name: str=None, age: int=None, gender: bool=None, description:str=None,image: str=None, encoding:list=None):
        self.name = name
        self.age=age
        self.gender = gender
        self.description=description
        self.image = image
        self.encoding=encoding if encoding!=None else self.initialize_encoding(image)
    def initialize_encoding(self,image):
        img = Image.open(image)
        face_encoding = mtcnn(img).to(device)
        face_encoding = resnet(face_encoding).to(device)
        return face_encoding
    # 오버라이딩
    def __deepcopy__(self, memo):
       
        copied_tensor = self.encoding.clone().detach()

        new_instance = Criminal(self.name, self.age, self.gender, self.description, self.image, self.encoding)
        return new_instance
