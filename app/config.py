import os

class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = ""
    SECRET_KEY = os.environ.get('SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = ""