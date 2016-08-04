import os
import sys

from app import app
from flask import render_template, redirect, url_for, send_from_directory
from flask import session, request, make_response
from flask import abort, flash
from jinja2.exceptions import TemplateNotFound
from werkzeug.exceptions import NotFound


AVAILABLE_APIS = [2015, 2016, 2017]

def check_available_years(filename):
    available_in = []
    for year in AVAILABLE_APIS:
        cwd = app.config['BASEDIR']
        fullpath = '{}/{}/{}/{}'.format(cwd, app.template_folder,
                                        year, filename)
        # import ipdb; ipdb.set_trace()
        if os.path.exists(fullpath):
            available_in.append(year)
    return available_in


@app.route('/')
@app.route('/index.html', methods=['GET'])
def index():
    title = 'Revit API Docs'
    # flash('Loaded')
    return render_template('index.html', title=title)


# API: /2015/
# API Pages: /2015/123sda-asds-asd.htmll
@app.route('/<string:year>/', methods=["GET"])
@app.route('/<string:year>/<path:html_path>', methods=["GET"])
def api_year(year, html_path=None):
    """Add Docs"""
    ns_template = 'ns_{year}.html'.format(year=year)
    active_ul = None
    
    if html_path:
        content_path = '{year}/{html}'.format(year=year, html=html_path)
        available_in = check_available_years(html_path)
        active_ul = html_path
    else:
        content_path = 'new_{year}.html'.format(year=year)
        available_in = AVAILABLE_APIS
    try:
        return render_template('api.html', year=year, active_ul=active_ul,
                               ns_template=ns_template, content=content_path,
                               available_in=available_in)
    except TemplateNotFound as error:
        """Must handle it since { include } inside template is generated
        dynamically by request path"""
        abort(404)


# This handles the static files form the .CHM content
@app.route('/favicon.ico', methods=["GET"])
@app.route('/icons/<string:filename>', methods=["GET"])
@app.route('/scripts/<string:filename>', methods=["GET"])
@app.route('/styles/<string:filename>', methods=["GET"])
def chm_static_redirect(filename=None):
    path = '/static' + request.path
    return redirect(path, 301)
