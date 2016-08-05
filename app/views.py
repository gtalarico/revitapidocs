import os
import sys

from flask import render_template, redirect, url_for, send_from_directory
from flask import session, request, make_response
from flask import abort, flash
from jinja2.exceptions import TemplateNotFound
from werkzeug.exceptions import NotFound

from app import app
from app.logger import logger
from app.utils import *


@app.route('/')
@app.route('/index.html', methods=['GET'])
def index():
    title = 'Revit API Docs'
    # flash('Loaded')
    return render_template('index.html', title=title)


# API: /2015/
# API Pages: /2015/123sda-asds-asd.htmll
@app.route('/<string:year>/', methods=["GET"])
@app.route('/<string:year>/<path:filename>', methods=["GET"])
def api_year(year, filename=None):
    """Add Docs"""
    ns_template = 'ns_{year}.html'.format(year=year)
    active_ul = None

    if filename:
        content_path = '{year}/{html}'.format(year=year, html=filename)
        available_in = check_available_years(filename)
        active_ul = filename
        schema = get_schema(year, filename)
    else:
        content_path = 'new_{year}.html'.format(year=year)
        available_in = AVAILABLE_APIS
        schema = {'name': "What's New"}
    try:
        logger.debug('Schema: %s', schema)
        return render_template('api.html', year=year, active_ul=active_ul,
                               ns_template=ns_template, content=content_path,
                               available_in=available_in, schema=schema)

    except TemplateNotFound as error:
        """Must handle it since { include } inside template is generated
        dynamically by request path"""
        logger.error('Template not found. Path: %s', request.path)
        abort(404)


# This handles the static files form the .CHM content
@app.route('/favicon.ico', methods=["GET"])
@app.route('/icons/<string:filename>', methods=["GET"])
@app.route('/scripts/<string:filename>', methods=["GET"])
@app.route('/styles/<string:filename>', methods=["GET"])
def chm_static_redirect(filename=None):
    path = '/static' + request.path
    return redirect(path, 301)
