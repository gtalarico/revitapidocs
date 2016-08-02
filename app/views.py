import os
import sys

from app import app
from flask import render_template, flash, redirect, url_for, session, request, make_response
from flask import abort


@app.before_request
def before_request():
    pass
    # g.user = current_user


@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    title = 'Revit API Docs'
    # flash('Loaded')
    return render_template('index.html', title=title)


@app.route('/<int:year>/', methods=["GET"])
def api_new(year):
    title = 'Revit API Docs: ' + str(year)
    namespace_year = 'ns_{year}.html'.format(year=year)
    content = 'new_{year}.html'.format(year=year)

    return render_template('api.html', title=title, active=str(year),
                           namespace_year=namespace_year,
                           content=content)


# API Pages: /2015/123sda-asds-asd.htmll
@app.route('/<int:year>/<path:path>', methods=["GET"])
def api_year(year, path):
    """Add Docs"""
    title = 'Revit API ' + str(year)
    html_path = '{year}/{path}'.format(year=year, path=path)
    namespace_year = 'ns_{year}.html'.format(year=year)

    return render_template('api.html', title=title, active=str(year),
                           namespace_year=namespace_year,
                           content=html_path, active_ul=path)



# Need to search and replace to it's served by guinicorn
# Some icons not being served.
@app.route('/<path:folder>/<path:path>', methods=["GET"])
def static_proxy(folder, path):
    if folder in ['scripts', 'styles', 'icons']:
        try:
            return app.send_static_file(os.path.join(folder, path))
        except:
            print('File not found: {}/{}'.format(folder, path))
    abort(404)
