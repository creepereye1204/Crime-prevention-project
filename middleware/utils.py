from fastapi import HTTPException
from PIL import Image
import shutil
from uuid import uuid4
import os
IMAGE_DIR = os.path.join("resource", "image")


def change_file_name(image):
    unique_filename = f"{uuid4()}.{image.filename.split('.')[-1]}"

   
    save_path = os.path.join("resource", "image", unique_filename)

    
    with open(save_path, "wb") as buffer:
        buffer.write(image.file.read())

    return save_path

