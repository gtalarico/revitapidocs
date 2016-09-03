import os
from bs4 import BeautifulSoup

from app import app, cache
from app.logger import logger

AVAILABLE_APIS = ['2015', '2016', '2017']


@cache.cached(timeout=86400)
def check_available_years(filename):
    available_in = []
    for year in AVAILABLE_APIS:
        template_dir = app.config['TEMPLATEDIR']
        fullpath = '{}/{}/{}'.format(template_dir, year, filename)

        if os.path.exists(fullpath):
            available_in.append(year)
    return available_in


@cache.cached(timeout=86400)
def get_schema(*path):
    """This should be stored/cached in database"""
    template_dir = app.config['TEMPLATEDIR']
    filepath = '/'.join(path)
    fullpath = '{}/{}'.format(template_dir, filepath)
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
            # description = soup.find(id='mainBody').find('div', { "class": "summary"}).text.strip()
            # Pages that have no summary description return symbol "A"
            # If description is too short (< 3), name is used instead
            if len(description) < 3 or len(description) > 300:
                description = 'Documenation of {}'.format(name)
            namespace = soup.find(id='mainBody').find('a').text.strip()
        except AttributeError as errmsg:
            logger.error(errmsg)
        else:
            return {'name': name,
                    'description': description,
                    'namespace': namespace}
    logger.error('Failed to get schema:: %s', fullpath)
    return
