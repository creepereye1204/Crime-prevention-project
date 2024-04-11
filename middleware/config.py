import os
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.environ.get('client-id',None)
CLIENT_SECRET = os.environ.get('client-secret',None)
SECRET_KEY = os.environ.get('secret-key',None)

URL = os.environ.get('db',None)+os.environ.get('root',None)+os.environ.get('password',None)\
    + os.environ.get('url',None)+os.environ.get('port',None)+os.environ.get('database',None)
