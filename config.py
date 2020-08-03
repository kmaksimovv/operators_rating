import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '7d441f27d441f27567d441f2b6176a'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LISTINGS_PER_PAGE = 15
    LANGUAGES = ['en', 'ru']

class DevelopementConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI') or \
        'mysql+pymysql://flask:flask@localhost/operators_rating'

    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI') or \
    #     'mysql+pymysql://devel:devel@172.16.29.5/asteriskcdrdb'


class TestingConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or \
			      'mysql+pymysql://flask:flask@localhost/operators_rating'


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or \
	'mysql+pymysql://flask:flask@localhost/operators_rating'
