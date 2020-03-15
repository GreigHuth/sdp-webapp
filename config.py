import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):

    MAX_DESKS = 2 

    V_HOST = "192.168.105.3"
    V_PORT = 5000

    N_HOST = "pichu"
    N_PORT = 5001

    A_HOST = "pichu"
    A_PORT = 5002

    SUCCESS_MSG = 1
    FAIL_MSG = 0
    
    #Key config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'bums'

    #db config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True