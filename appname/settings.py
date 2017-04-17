"""
Appname settings
"""

import tempfile
db_file = tempfile.NamedTemporaryFile()


class Config(object):
    "Basic config"
    SECRET_KEY = 'REPLACE ME'


class ProdConfig(Config):
    "Production config"
    ENV = 'prod'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/prod.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_TYPE = 'simple'


class DevConfig(Config):
    "Develop config"
    ENV = 'dev'
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/dev.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_TYPE = 'null'
    ASSETS_DEBUG = True


class TestConfig(Config):
    "Test config"
    ENV = 'test'
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_file.name + '.db'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_TYPE = 'null'
    WTF_CSRF_ENABLED = False
