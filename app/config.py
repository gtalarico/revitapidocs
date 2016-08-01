import os

class Config(object):
    DEBUG = False
    TESTING = False
    # DATABASE_URI = 'sqlite://:memory:'
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

class ProductionConfig(Config):
    SECRET_KEY = os.getenv('SECRET_KEY')
    if SECRET_KEY is None:
        raise ValueError('SECRET_KEY not set.')

    # DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = '*)(EFUELKH!@#(&!_@&UQPasdasdj!(@&$_EFSDPFJSLK!@!@#1231)))'


production = int(os.getenv('PRODUCTION'))

if not production:
    print('Development Config')
    print('PRODUCTION={}'.format(production))
    config = DevelopmentConfig

else:
    print('Running on Heroku')
    config = ProductionConfig
