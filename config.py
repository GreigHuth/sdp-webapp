import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    MAX_SEARCH_RESULTS = 50

    MAX_DESKS = 2 

    ELASTICSEARCH_URL = "http://localhost:9200"
    WHOOSH_BASE = os.path.join(basedir, 'search.db')

    #Key config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'bums'

    #db config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True