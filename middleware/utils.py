from fastapi import HTTPException
from PIL import Image
import shutil
from uuid import uuid4
import os
IMAGE_DIR = os.path.join("resource", "image")

# uuid4를 사용하여 무작위 UUID 생성
def change_file_name(file):


        # UUID4를 사용하여 고유한 파일 이름 생성
    filename = f"{uuid4()}.jpg"
    file_path = os.path.join(IMAGE_DIR, filename)

    # 파일 저장
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": filename}


