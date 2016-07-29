'''import main Flask. This starts when run.py calls from app import app'''
import os
from flask import Flask
# from flask.ext.sqlalchemy import SQLAlchemy
# from flask.ext.login import LoginManager
# from flask.ext.bcrypt import Bcrypt
# from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView
# from flask.ext.babel import Babel

app = Flask(__name__)
# db = SQLAlchemy(app)
# login_manager = LoginManager()
# login_manager.init_app(app)
# bcrypt = Bcrypt(app)

from app import config, views
# from app import models

app.config.from_object(config)

