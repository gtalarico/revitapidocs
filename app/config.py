import os


class Config(object):
    DEBUG = False
    TESTING = False
    # DATABASE_URI = 'sqlite://:memory:'
    BASEDIR = os.path.abspath(os.path.dirname(__file__))


class ProductionConfig(Config):
    SECRET_KEY = os.getenv('SECRET_KEY', None)
    # DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = '*)(EFUELKH!@#(&!_@&UQPasdasdj!(@&$_EFSDPFJSLK!@!@#1231)))'


production = bool(int(os.getenv('PRODUCTION', 0)))
print('PRODUCTION={}'.format(production))

if not production:
    print('DEVELOPMENT CONFIG')
    config = DevelopmentConfig

else:
    print('PRODUCTION CONFIG - HEROKU')
    config = ProductionConfig
