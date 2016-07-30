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


@app.route('/<int:year>')
def api(year):
    flash(year)
    title = 'Revit API ' + str(year)
    return render_template('base.html', title=title, active=str(year))
    # return render_template('whatsnew.html', title=title)


# @app.route('/2015/')
# @app.route('/2015/html/<path:path>')
# def api_2015(path):
#     # return render_template('docs/2015/{path}'.format(path=path))
#     content_path = 'docs/2015/{}'.format(path)
#     return render_template('base.html', content_path=content_path)


# Need to search and replace to it's served by guinicorn
# @app.route('/2015/<path:path>')
# def static_proxy(path):
  # send_static_file will guess the correct MIME type
  # return app.send_static_file('path)
  # return send_static_file(path)
