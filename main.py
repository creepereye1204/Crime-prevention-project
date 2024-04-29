import copy

from fastapi import Request,HTTPException
from fastapi.responses import StreamingResponse

from app.src.middleware.utils import change_file_name
from jobs.predict import *
from app.src.middleware.settings import *
from starlette.responses import RedirectResponse
import uvicorn
import threading
from dataset.schema import *
from middleware.settings import *
from app.src.middleware import settings


from fastapi import FastAPI, File, UploadFile, Form
from app.src.middleware.settings import *


@app.get('/')
async def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/login")
async def login(request: Request):
    url = request.url_for("auth")
    return await oauth.google.authorize_redirect(request,url)

@app.get('/logout')
async def logout(request: Request):
    request.session.pop('user')
    return RedirectResponse('/')
@app.get("/auth")
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        return templates.TemplateResponse(
            name='error.html',
            context={'request':request,'error':e.error}
        )

    user= token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    return templates.TemplateResponse('wellcome.html',{'request':request,'user':dict(user)})



@app.get("/criminal")
async def criminal(request: Request):
    return templates.TemplateResponse('add.html',{'request':request})

@app.post("/criminal/add")
async def add_criminal(
    name: str = Form(...),
    age: int = Form(...),
    gender: bool = Form(...),
    description: str = Form(...),
    image: UploadFile = File(...)
    ):
    try:
        img = Image.open(image.file)
        img.verify()  # 이미지 파일인지 확인
        image.file.seek(0)
        path=change_file_name(image=image)
        try:
            db.add(CriminalDao(name=name, age=age, gender=gender, description=description, image=path))
            db.commit()
            settings.known_faces.append(Criminal(name=name, age=age, gender=gender, description=description, image=path))
            settings.shared_known_faces=[copy.deepcopy(t) for t in settings.known_faces]
        except:
            db.rollback()  # 오류 발생 시 롤백
            raise
        # finally:
        #     db.close()  # 세션 닫기

    except (IOError, SyntaxError) as e:
        raise HTTPException(status_code=400, detail=f"Uploaded file is not a valid image and {e.error}")

    return RedirectResponse('/criminal')







@app.get("/video")
async def video(request: Request):
    return templates.TemplateResponse("streaming.html", {"request": request})

@app.get("/video/stream")
async def stream():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")



if __name__ == '__main__':
    threading.Thread(target=recognize_faces_in_video, daemon=True).start()
    uvicorn.run("main:app", port=5000)