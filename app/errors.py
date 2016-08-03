from flask import render_template, request
from app import app
from app.logger import logger


@app.errorhandler(404)
def page_not_found(error):
    logger.error('404 SERVER ERROR AT: {}'.format(request.path))
    logger.error('ERROR: {}|{}'.format(error.code, error.name))
    return render_template('error.html', error=error), 404


@app.errorhandler(500)
def server_error(error):
    logger.error('500 SERVER ERROR AT: {}'.format(request.path))
    logger.error('ERROR: {}|{}'.format(error.code, error.name))
    return render_template('error.html', error=error), 500
