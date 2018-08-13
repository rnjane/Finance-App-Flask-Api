import os

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


class Config(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE')


# NOTE: Instead of having a fourth ProductionConfig class, having the parent
# Config class have production configurations by default is much drier

configuration = {
    'production': Config,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
}
