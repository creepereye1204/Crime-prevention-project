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

    def __deepcopy__(self, memo):
        # 텐서의 경우, clone() 메서드를 사용하여 복사하고, detach()로 계산 그래프에서 분리합니다.
        # 필요한 경우, .to() 메서드를 사용하여 원하는 디바이스로 텐서를 옮길 수도 있습니다.
        copied_tensor = self.encoding.clone().detach()
        # 새로운 인스턴스를 생성하여 복사된 텐서를 할당합니다.
        new_instance = Criminal(self.name, self.age, self.gender, self.description, self.image, self.encoding)
        return new_instance