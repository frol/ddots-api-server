# pylint: disable=too-few-public-methods,invalid-name,missing-docstring
import os


class BaseConfig(object):
    SECRET_KEY = 'this-really-needs-to-be-changed'

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % (os.path.join(PROJECT_ROOT, "ddots.db"))

    DEBUG = False
    ERROR_404_HELP = False
    VERSION = os.environ.get('DDOTS_VERSION', '1.x.y')

    AUTHORIZATIONS = {
        'oauth2_password': {
            'type': 'oauth2',
            'flow': 'password',
            'scopes': {},
            'tokenUrl': '/auth/oauth2/token',
        },
        # TODO: implement other grant types for third-party apps
        #'oauth2_implicit': {
        #    'type': 'oauth2',
        #    'flow': 'implicit',
        #    'scopes': {},
        #    'authorizationUrl': '/auth/oauth2/authorize',
        #},
    }

    ENABLED_MODULES = (
        'auth',

        'users',
        'teams',
        'problems',
        'programming_languages',
        'solutions',

        'api',
    )

    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

    SWAGGER_UI_JSONEDITOR = True
    SWAGGER_UI_OAUTH_CLIENT_ID = 'documentation'
    SWAGGER_UI_OAUTH_REALM = "Authentication for DDOTS API Server"
    SWAGGER_UI_OAUTH_APP_NAME = "DDOTS API Server"

    SEAWEEDFS_CONFIG = {
        'MASTER_ADDR': os.getenv('DDOTS_SEAWEEDFS_HOST', 'localhost'),
        'MASTER_PORT': int(os.getenv('DDOTS_SEAWEEDFS_PORT', 9333)),
    }

    # TODO: consider if these are relevant for this project
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    CSRF_ENABLED = True


class ProductionConfig(BaseConfig):
    SECRET_KEY = os.getenv('DDOTS_API_SERVER_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DDOTS_API_SERVER_SQLALCHEMY_DATABASE_URI')


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True
    #SQLALCHEMY_ECHO = True

    # Use in-memory SQLite database for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
