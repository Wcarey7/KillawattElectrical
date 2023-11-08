import os
from datetime import timedelta
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    TESTING = False
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_THRESHOLD = 50
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    REMEMBER_COOKIE_DURATION = timedelta(hours=24)
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    CUSTOMERS_PER_PAGE = 5


class TestConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'   # use an in-memory database for tests
    WTF_CSRF_ENABLED = False                # no CSRF during tests
    SESSION_FILE_THRESHOLD = 10


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'app.db')


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SECRET_KEY = os.environ.get('SECRET_KEY')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestConfig,
    'default': DevelopmentConfig
}
