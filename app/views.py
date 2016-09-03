import os
import sys
import json
import re
import requests
from collections import OrderedDict

from flask import render_template, redirect, url_for, send_from_directory
from flask import session, request, make_response
from flask import abort, flash, jsonify
from jinja2.exceptions import TemplateNotFound
from werkzeug.exceptions import NotFound

from app import app
from app import cache
from app.logger import logger
from app.utils import AVAILABLE_APIS
from app.utils import get_schema, check_available_years
from app.gists import get_gists


# @cache.cached(timeout=60)
@app.route('/')
@app.route('/index.html', methods=['GET'])
def index():
    title = 'Revit API Docs'
    return render_template('index.html', title=title)

# API: /2015/
# API Pages: /2015/123sda-asds-asd.htmll
@cache.cached(timeout=600)
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
    elif year in AVAILABLE_APIS:
        content_path = 'home.html'
        available_in = AVAILABLE_APIS
        schema = {'name': "Revit API {} Index".format(year),
                  'description': 'Full Online Documenation for Revit API {}'.format(year)}
    else:
        abort(404)
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


@cache.cached(timeout=604800)  # 1 Week
@app.route('/<string:year>/namespace.json', methods=['GET'])
def namespace_get(year):
    cwd = app.config['BASEDIR']
    filename = 'ns_{year}.json'.format(year=year)
    fullpath = '{}/{}/{}/{}'.format(cwd, app.template_folder,
                                    'json', filename)
    with open(fullpath) as fp:
        j = json.load(fp)
    return jsonify(j)


# Not Cached to Prevent High Memory Usage
@app.route('/<string:year>/search', methods=['GET'])
def namespace_search(year):
    cwd = app.config['BASEDIR']
    filename = 'members_{year}.json'.format(year=year)
    fullpath = '{}/{}/{}/{}'.format(cwd, app.template_folder, 'json', filename)
    with open(fullpath) as fp:
        members = json.load(fp, object_pairs_hook=OrderedDict)
    results = []
    NO_RESULTS_RESPONSE = [{'name':'No Results', 'link': '#'}]
    query = request.args.get('query')
    query = re.sub(r'\s', r'(\s)?', query)
    if not query:
        return jsonify(NO_RESULTS_RESPONSE)
    for name, href in members.items():
        match = re.findall(query.lower(), name.lower())
        if match:
            results.append({'name': name, 'link': href})
    if not results:
        results = NO_RESULTS_RESPONSE
    return jsonify(results)


# This handles the static files form the .CHM content
@cache.cached(timeout=86400)
@app.route('/favicon.ico', methods=["GET"])
@app.route('/icons/<string:filename>', methods=["GET"])
@app.route('/scripts/<string:filename>', methods=["GET"])
@app.route('/styles/<string:filename>', methods=["GET"])
def chm_static_redirect(filename=None):
    path = '/static' + request.path
    return redirect(path, 301)


@app.after_request
def add_header(response):
    config_cache = app.config['SEND_FILE_MAX_AGE_DEFAULT']
    response.headers['Cache-Control'] = 'public, max-age={}'.format(config_cache)
    return response


@app.route('/python/', methods=['GET'])
def python():
    # ordered_gist = OrderedDict(sorted(get_gists().items()))
    gists_by_categories = get_gists()
    d = OrderedDict(sorted(gists_by_categories.items()))
    # d = {'error':'Nothing'}
    return render_template('python.html', gists_categories=d)
