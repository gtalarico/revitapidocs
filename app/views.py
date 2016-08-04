import os
import sys

from app import app
from flask import render_template, redirect, url_for, send_from_directory
from flask import session, request, make_response
from flask import abort, flash
from jinja2.exceptions import TemplateNotFound
from werkzeug.exceptions import NotFound


@app.route('/')
@app.route('/index.html', methods=['GET'])
def index():
    title = 'Revit API Docs'
    # flash('Loaded')
    return render_template('index.html', title=title)


# API: /2015/
# API Pages: /2015/123sda-asds-asd.htmll
@app.route('/<int:year>/', methods=["GET"])
@app.route('/<int:year>/<path:html_path>', methods=["GET"])
def api_year(year, html_path=None):
    """Add Docs"""
    title = 'Revit API ' + str(year)
    ns_template = 'ns_{year}.html'.format(year=year)

    if html_path:
        content_path = '{year}/{html}'.format(year=year, html=html_path)
        available_in_years = []
        for year in [2015, 2016, 2017]:
            if os.path.exists('{}/{}'.format(app.template_folder, year)):
                available_in_years.append(year)

    else:
        content_path = 'new_{year}.html'.format(year=year)
    try:
        return render_template('api.html', title=title, active=str(year),
                               ns_template=ns_template,
                               content=content_path,
                               active_ul=html_path)
    except TemplateNotFound as error:
        """Must handle it since { include } inside template is generated
        dynamically by request path"""
        abort(404)


# This handles the static files form the .CHM content
@app.route('/icons/<string:filename>', methods=["GET"])
@app.route('/scripts/<string:filename>', methods=["GET"])
@app.route('/styles/<string:filename>', methods=["GET"])
def chm_static_redirect(filename):
    path = '/static' + request.path
    return redirect(path, 301)
