from app.src.dataset.data_manager import *
from starlette.templating import Jinja2Templates
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from authlib.integrations.starlette_client import OAuth,OAuthError
from starlette.middleware.sessions import SessionMiddleware


from app.src.middleware.config import *
from app.src.models.database import *




app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

oauth=OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    client_kwargs={'scope':'email openid profile',
                   'redirect_uri':'http://localhost:5000/auth'
                   }
)



app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")



engine = create_engine(URL,encoding='utf8')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


criminals=session.query(CriminalDao).all()


known_faces = load_known_faces(criminals)