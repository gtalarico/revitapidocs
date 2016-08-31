import os
from collections import defaultdict
from bs4 import BeautifulSoup
from github import Github

from app import app
from app.logger import logger

AVAILABLE_APIS = ['2015', '2016', '2017']

oauth = '94e9d489cc282b34a41c9ea89a3c0f396fb42f58'
github = Github(oauth)
github_user = github.get_user()
gist_pages = github_user.get_gists()

def check_available_years(filename):
    available_in = []
    for year in AVAILABLE_APIS:
        template_dir = app.config['TEMPLATEDIR']
        fullpath = '{}/{}/{}'.format(template_dir, year, filename)

        if os.path.exists(fullpath):
            available_in.append(year)
    return available_in


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


def get_gists():
    # github.get_api_status().rate.remaining
    # except requests.exceptions.RequestException as errmsg:
    #     logger.warning('Failed to get GISTS: %s', errmsg)
    #     gists_by_categories = {'error': errmsg.__doc__}
    gists_by_categories = defaultdict(list)
    # gists= []
    for gist in gist_pages:
        if 'RevitAPI' in gist.description:
            # gists.append(gist)
            gist_group, gist_name = gist.description.split('::')[1:]
            gist_embed_url = '{url}.js'.format(url=gist.html_url)
            gists_by_categories[gist_group].append({'name': gist_name,
                                                    'url': gist_embed_url})
        # GISTS_URL = 'https://api.github.com/users/gtalarico/gists'
    # try:
    #     gists = requests.get(GISTS_URL, timeout=(1, 1.5))
    # else:
    #
    #     if gists.status_code != 200:
    #         logger.error('Gist Get Failed. Status Code: %s', gists.status_code)
    #         gists_by_categories = {'error': 'Could not get Gists from Github. '}
    #     else:# add handler for other error codes
    #         json_gists = json.loads(gists.text)  # Json Gists
    #
    #         sorted_gists = sorted(json_gists, key=lambda k: k['description'])
    #         for gist in sorted_gists:
    #             if 'RevitAPI' not in gist['description']:
    #                 continue
    #             gist_group, gist_name = gist['description'].split('::')[1:]
    #             gist_embed_url = '{url}.js'.format(url=gist['html_url'])
    #             gists_by_categories[gist_group].append({'name': gist_name,
    #                                                     'url': gist_embed_url})
    return gists_by_categories
    # return gists_by_categories

# def get_gists():
#
#     GISTS_URL = 'https://api.github.com/users/gtalarico/gists'
#     try:
#         gists = requests.get(GISTS_URL, timeout=(1, 1.5))
#     except requests.exceptions.RequestException as errmsg:
#         logger.warning('Failed to get GISTS: %s', errmsg)
#         gists_by_categories = {'error': errmsg.__doc__}
#     else:
#         gists_by_categories = defaultdict(list)
#
#         if gists.status_code != 200:
#             logger.error('Gist Get Failed. Status Code: %s', gists.status_code)
#             gists_by_categories = {'error': 'Could not get Gists from Github. '}
#         else:# add handler for other error codes
#             json_gists = json.loads(gists.text)  # Json Gists
#
#             sorted_gists = sorted(json_gists, key=lambda k: k['description'])
#             for gist in sorted_gists:
#                 if 'RevitAPI' not in gist['description']:
#                     continue
#                 gist_group, gist_name = gist['description'].split('::')[1:]
#                 gist_embed_url = '{url}.js'.format(url=gist['html_url'])
#                 gists_by_categories[gist_group].append({'name': gist_name,
#                                                         'url': gist_embed_url})
#     return gists_by_categories
