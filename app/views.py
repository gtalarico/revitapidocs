import os
import sys
import json
import re
from flask import render_template, redirect, url_for, send_from_directory
from flask import session, request, make_response
from flask import abort, flash, jsonify
from jinja2.exceptions import TemplateNotFound
from werkzeug.exceptions import NotFound

from app import app, cache
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
    active_href = filename

    if filename:
        content_path = '{year}/{html}'.format(year=year, html=filename)
        available_in = check_available_years(filename)
        active_href = filename
        schema = get_schema(year, filename)
    else:
        content_path = 'home.html'
        available_in = AVAILABLE_APIS
        schema = {'name': "Revit API {} Index".format(year)}
    try:
        logger.debug('Schema: %s', schema)
        return render_template('api.html', year=year, active_href=active_href,
                               content=content_path,
                               available_in=available_in, schema=schema)

    except TemplateNotFound as error:
        """Must handle it since { include } inside template is generated
        dynamically by request path"""
        logger.error('Template not found. Path: %s', request.path)
        abort(404)


@cache.cached(timeout=600)
@app.route('/<string:year>/namespace.json', methods=['GET'])
def namespace_get(year):
    cwd = app.config['BASEDIR']
    filename = 'ns_{year}.json'.format(year=year)
    fullpath = '{}/{}/{}/{}'.format(cwd, app.template_folder,
                                    'json', filename)
    with open(fullpath) as fp:
        j = json.load(fp)
    return jsonify(j)


@app.route('/<string:year>/search', methods=['GET'])
def namespace_search(year):
    cwd = app.config['BASEDIR']
    filename = 'members_{year}.json'.format(year=year)
    fullpath = '{}/{}/{}/{}'.format(cwd, app.template_folder, 'json', filename)
    with open(fullpath) as fp:
        members = json.load(fp)
    results = []
    query = request.args.get('query')
    if not query:
        return jsonify([])
    for name, href in members.items():
        match = re.findall(query.lower(), name.lower())
        if match:
            results.append({'name': name, 'link': href})
    return jsonify(results)


# This handles the static files form the .CHM content
@app.route('/favicon.ico', methods=["GET"])
@app.route('/icons/<string:filename>', methods=["GET"])
@app.route('/scripts/<string:filename>', methods=["GET"])
@app.route('/styles/<string:filename>', methods=["GET"])
def chm_static_redirect(filename=None):
    path = '/static' + request.path
    return redirect(path, 301)
