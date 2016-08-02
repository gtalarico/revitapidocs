from app import app
from flask import render_template

@app.errorhandler(404)
def page_not_found(e):
    errormsg = e
    return render_template('error.html', errormsg=errormsg), 404


@app.errorhandler(500)
def server_error(e):
    errormsg = e
    return render_template('error.html', errormsg=errormsg), 500
