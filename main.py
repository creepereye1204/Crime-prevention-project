from fastapi import Request
from fastapi.responses import StreamingResponse
from jobs.predict import *
from app.src.middleware.settings import *
from starlette.responses import RedirectResponse
import uvicorn
import threading


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


@app.get("/video")
async def video(request: Request):
    return templates.TemplateResponse("streaming.html", {"request": request})

@app.get("/video/stream")
async def stream():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")



if __name__ == '__main__':
    threading.Thread(target=recognize_faces_in_video, daemon=True).start()
    uvicorn.run("main:app", port=5000)


