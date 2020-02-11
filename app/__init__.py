from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import paramiko

#init app and config
app = Flask(__name__)
app.config.from_object(Config)

#init SSH client
ssh_client = paramiko.SSHClient()

#init database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models