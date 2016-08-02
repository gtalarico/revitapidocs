'''import main Flask. This starts when run.py calls from app import app'''
import os
from flask import Flask
from flask_compress import Compress
app = Flask(__name__)
Compress(app)

from app import views, seo_response, errors
from app.config import config
app.config.from_object(config)
