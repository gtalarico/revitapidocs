import os
import sys
import json
import re
import requests
from collections import OrderedDict, defaultdict

from flask import render_template, redirect, url_for, send_from_directory
from flask import session, request, make_response
from flask import abort, flash, jsonify
from jinja2.exceptions import TemplateNotFound
from werkzeug.exceptions import NotFound

from app import app
from app import cache
from app.logger import logger
from app.utils import *


# @cache.cached(timeout=60)
@app.route('/')
@app.route('/index.html', methods=['GET'])
def index():
    title = 'Revit API Docs'
    return render_template('index.html', title=title)


# API: /2015/
# API Pages: /2015/123sda-asds-asd.htmll
# @cache.cached(timeout=3600)
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
        schema = {'name': "Revit API {} Index".format(year)}
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


# @cache.cached(timeout=3600)
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
        members = json.load(fp, object_pairs_hook=OrderedDict)
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


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'public, max-age=3600'
    return response

@app.route('/python/', methods=['GET'])
def python():
    # ordered_gist = OrderedDict(sorted(get_gists().items()))
    gists_by_categories = get_gists()
    d = OrderedDict(sorted(gists_by_categories.items()))
    return render_template('python.html', gists_categories=d)

# @app.route('/gists/gists.json', methods=['GET'])
def get_gists():
    GISTS_URL = 'https://api.github.com/users/gtalarico/gists'
    gists = requests.get(GISTS_URL)
    gists_by_categories = defaultdict(list)

    if gists.status_code == 200:
        json_gists = json.loads(gists.text) # Json Gists

        sorted_gists = sorted(json_gists, key=lambda k: k['description'])
        for gist in sorted_gists:
            if 'RevitAPI' not in gist['description']:
                continue
            gist_group, gist_name = gist['description'].split('::')[1:]
            gist_embed_url = '{url}.js'.format(url=gist['html_url'])
            gists_by_categories[gist_group].append({'name': gist_name,
                                                    'url': gist_embed_url})
    return gists_by_categories
    # return jsonify(revit_api_gists)
