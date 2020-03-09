import os

class Config(object):
    DEBUG = False
    MONGODB_SETTINGS = {
        'host': 'mongodb://localhost/CollegeRank'
    }

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    MONGODB_SETTINGS = {
        'host': os.environ.get('MONGODB_HOST')
    }