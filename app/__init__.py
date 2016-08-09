'''import main Flask. This starts when run.py calls from app import app'''
import os
from flask import Flask
from flask_compress import Compress
from flask_assets import Bundle, Environment
from flask_cache import Cache

from app.assets import css_assets, js_assets
from app.assets import css_chm, js_chm
from app.logger import logger

app = Flask(__name__)
Compress(app)
cache = Cache(app,config={'CACHE_TYPE': 'simple'})

# ASSETS
assets = Environment(app)
assets.debug = bool(int(os.environ.get('ASSETS_DEBUG', False)))
assets.register('css_assets', css_assets)
assets.register('js_assets', js_assets)
assets.register('css_chm', css_chm)
assets.register('js_chm', js_chm)
logger.info('ASSETS DEBUG: {}'.format(assets.debug))


from app import views, seo_response, errors
from app import assets
from app.config import config
app.config.from_object(config)
