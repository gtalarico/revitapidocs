import os
import sys

from app import app
from flask import render_template, redirect, url_for, send_from_directory
from flask import session, request, make_response
from flask import abort, flash
from jinja2.exceptions import TemplateNotFound
from werkzeug.exceptions import NotFound


@app.before_request
def before_request():
    pass
    # g.user = current_user


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
        content = '{year}/{html}'.format(year=year, html=html_path)
    else:
        content = 'new_{year}.html'.format(year=year)

    try:
        return render_template('api.html', title=title, active=str(year),
                               ns_template=ns_template,
                               content=content,
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


# Need to search and replace to it's served by guinicorn
# Some icons not being served.
# @app.route('/<path:folder>/<path:filename>', methods=["GET"])
# def static_proxy(folder, filename):
#     if folder in ['scripts', 'styles', 'icons']:
#         try:
#             return app.send_static_file(filename)
#             # On windows this method fails on the safe_join
#             # return app.send_static_file(os.path.join(folder, path))
#         except NotFound:
#             try:
#                 '''On Windows, this is required'''
#                 folder = os.path.join('static', folder)
#                 return send_from_directory(folder, filename)
#             except NotFound:
#                 abort(404)
