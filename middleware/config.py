import os
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.environ.get('client-id',None)
CLIENT_SECRET = os.environ.get('client-secret',None)
SECRET_KEY = os.environ.get('secret-key',None)

URL = os.environ.get('database',None)
