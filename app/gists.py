from collections import defaultdict
from github import Github
from github.GithubException import GithubException

from app import app, cache
from app.logger import logger


class GistWrapper:
    """ Singleton Wrapper Class. Serves 2 functions:
    - Simplify and abstract PyGithub check_available_years
    - Add ensure single session is created"""

    OAUTH = app.config.get('GITHUB_TOKEN')
    class __GistWrapper:
        def __init__(self):
            logger.info('Initializing Gist Session')
            self._session = Github(GistWrapper.OAUTH, per_page=100)
            try:
                self._session.get_user().id
            except Exception as errmsg:
                logger.error('GitWrapper Error:')
                self.nullify_session(errmsg)
            else:
                self.update_rates()
                self._user = self._session.get_user()
                self.pages = self._user.get_gists()
                self.limit = self._session.get_rate_limit().rate.limit
                logger.info('Rate Limit: {}/{}'.format(self.remaining,
                                                       self.limit))
                if self.limit < 1:
                    self.nullify_session()
        def nullify_session(self, errmsg):
            # Sets Variables to ensure error handling

            logger.info(errmsg)
            self.pages = []
            self.remaining = 0
            self.limit = 0
            self.error = errmsg

        def update_rates(self):
            self.remaining = self._session.get_rate_limit().rate.remaining

        def update_pages(self):
            self.pages = self._user.get_gists()

    instance = None
    def __init__(self):
        if not GistWrapper.instance:
            GistWrapper.instance = GistWrapper.__GistWrapper()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __bool__(self):
        return bool(self.instance.pages)


@cache.cached(timeout=43200, key_prefix='gists')  # 12 Hour
def get_gists():
    github_gist = GistWrapper()
    logger.info('Gettings Gists. Rate: {}/{}'.format(github_gist.remaining,
                                                  github_gist.limit))
    if not github_gist:
        return {'error': github_gist.error}

    gists_by_categories = defaultdict(list)
    for gist in github_gist.pages:

        if 'RevitAPI' in gist.description:
            gist_group, gist_name = gist.description.split('::')[1:]
            gist_embed_url = '{url}.js'.format(url=gist.html_url)
            gists_by_categories[gist_group].append({'name': gist_name,
                                                    'url': gist_embed_url})
    return gists_by_categories
