import os
from bs4 import BeautifulSoup

from app import app
from app.logger import logger

AVAILABLE_APIS = ['2015', '2016', '2017']

def check_available_years(filename):
    available_in = []
    for year in AVAILABLE_APIS:
        cwd = app.config['BASEDIR']
        fullpath = '{}/{}/{}/{}'.format(cwd, app.template_folder,
                                        year, filename)

        if os.path.exists(fullpath):
            available_in.append(year)
    return available_in


def get_schema(*path):
    """This should be stored/cached in database"""
    cwd = app.config['BASEDIR']
    filepath = '/'.join(path)
    fullpath = '{}/{}/{}'.format(cwd, app.template_folder, filepath)
    logger.debug('Getting schema for : %s', fullpath)
    try:
        with open(fullpath) as fp:
            soup = BeautifulSoup(fp.read(), 'html.parser')
    except IOError as errmsg:
        logger.error(errmsg)
    else:
        try:
            name = soup.title.string.strip()
            description = soup.find(id='mainBody').find('div').text.strip()
            namespace = soup.find(id='mainBody').find('a').text.strip()
        except AttributeError as errmsg:
            logger.error(errmsg)
        else:
            return {'name': name,
            'description': description,
            'namespace': namespace}
    logger.error('Failed to get schema:: %s', fullpath)
    return
