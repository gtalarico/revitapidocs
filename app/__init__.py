'''import main Flask. This starts when run.py calls from app import app'''
import os
from flask import Flask
from flask_compress import Compress
from flask_assets import Bundle, Environment

from app.assets import css_assets, js_assets

app = Flask(__name__)
Compress(app)

# ASSETS
assets = Environment(app)
assets.debug = bool(int(os.environ.get('ASSETS_DEBUG', False)))
assets.register('css_assets', css_assets)
assets.register('js_assets', js_assets)
print('ASSETS DEBUG: {}'.format(assets.debug))


from app import views, seo_response, errors
from app import assets
from app.config import config
app.config.from_object(config)
