from fastapi import HTTPException
from PIL import Image
import shutil
from uuid import uuid4
import os
IMAGE_DIR = os.path.join("resource", "image")

# uuid4를 사용하여 무작위 UUID 생성
def change_file_name(image):
    unique_filename = f"{uuid4()}.{image.filename.split('.')[-1]}"

    # 저장할 경로 설정
    save_path = os.path.join("resource", "image", unique_filename)

    # 이미지 파일 저장
    with open(save_path, "wb") as buffer:
        buffer.write(image.file.read())

    return save_path

