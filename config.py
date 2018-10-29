import os
basedir = os.path.abspath(os.path.dirname(__file__))

from app.constants.hosting import HostingType


class Config(object):
    ENV = ''
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HOSTING = HostingType.local
    SQLALCHEMY_DATABASE_URI = ''
    CSRF_KEY = ''
    MAIL_SUBJECT_PREFIX = 'Your service name'
    COMPANY_NAME = 'Your company name' # Change to your company name
    TRIAL_PERIOD_IN_DAYS = 14 # Change to your trial (in days, it's 2 weeks by default). Put 0 if no trial


class ProductionConfig(Config):
    ENV = 'prod'
    DEBUG = False
    HOSTING = HostingType.google_app_engine

    # The values below MUST store in the hosting config variables
    #SQLALCHEMY_DATABASE_URI
    #SECRET_KEY
    #SECRET_SALT

class DevelopmentConfig(Config):
    ENV = 'dev'
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ['db_url'] # Store it in the hosting config
    SECRET_KEY = os.environ['secret_key'] # Store it in the hosting config
    SECRET_SALT = os.environ['secret_salt'] # Store it in the hosting config
    MAIL_SERVER = os.environ['mail_server']
    MAIL_PORT = os.environ['mail_port']
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ['mail_username']
    SECURITY_EMAIL_SENDER = os.environ['mail_username']
    MAIL_DEFAULT_SENDER = os.environ['mail_username']
    MAIL_PASSWORD = os.environ['mail_password']
    ADMIN_EMAIL = os.environ['admin_email']
    TRIAL_PERIOD_IN_DAYS = 1 # Change it or remove it


class TestingConfig(Config):
    ENV = 'test'
    TESTING = True

config = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'prod': ProductionConfig,
    'default' : DevelopmentConfig
}

class ConfigHelper:

    # Allows setting config from argument, or from "env" environment variable (see Activate.bat)

    @staticmethod
    def __check_config_name(env_name):
        return env_name is not None and env_name != '' and env_name in config is not None

    @staticmethod
    def set_config(args):
        if (args is not None and len(args) > 1):
            # Check argument
            if ConfigHelper.__check_config_name(args[1]):
                return config[args[1]]
        
        # Check os env var
        if ConfigHelper.__check_config_name(os.environ['env']):
            return config[os.environ['env']]

        # Nothing worked, return default config
        return config['default']
    