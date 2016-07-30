from app import app
from flask import render_template, flash, redirect, url_for, session, request, g
import sys


@app.before_request
def before_request():
    pass
    # g.user = current_user


@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    title = 'Revit API Docs'
    flash('Loaded')
    return render_template('index.html', title=title)


@app.route('/<int:year>/')
def api(year):
    title = 'Revit API ' + str(year)
    namespace_year = 'ns_{year}.html'.format(year=year)
    content = 'new_{year}.html'.format(year=year)

    return render_template('api.html', title=title, active=str(year),
                           namespace_year=namespace_year,
                           content=content)


@app.route('/<int:year>/<path:path>')
def api_2015(year, path):
    title = 'Revit API ' + str(year)
    html_path = '{year}/{path}'.format(year=year, path=path)
    namespace_year = 'ns_{year}.html'.format(year=year)

    return render_template('api.html', title=title, active=str(year),
                           namespace_year=namespace_year,
                           content=html_path, active_ul=path)


# Need to search and replace to it's served by guinicorn
@app.route('/<path:folder>/<path:path>')
def static_proxy(folder, path):
  import os
  return app.send_static_file(os.path.join(folder,path))
