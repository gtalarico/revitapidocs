from app import app
from flask import render_template, flash, redirect, url_for, session, request, g
# from flask.ext.login import login_user, logout_user, current_user, login_required
# from .forms import LoginForm, CreateAccountForm
# from .models import User
# from .util.security import ts, send_email
import sys


@app.before_request
def before_request():
    pass
    # g.user = current_user

@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    app.logger.info('Index View Called')
    # user = g.user
    title = 'Index'
    flash('Loaded')
    return render_template('index.html', title=title)
