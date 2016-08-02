'''import main Flask. This starts when run.py calls from app import app'''
import os

from flask import Flask
from flask_compress import Compress
from flask_assets import Environment, Bundle
from flask_cache import Cache

app = Flask(__name__)
Compress(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

from app.config import config
app.config.from_object(config)

from app import views
from app.assets import css_assets, js_assets, css_chm, js_chm

ASSETS_DEBUG = False
assets = Environment(app)
assets.register('css_assets', css_assets)
assets.register('js_assets', js_assets)
assets.register('css_chm', css_chm)
assets.register('js_chm', js_chm)
assets.debug = bool(int(os.getenv('ASSETS_DEBUG', 0))) or ASSETS_DEBUG
