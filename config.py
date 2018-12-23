import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    @staticmethod
    def get_secure_variable(var_name = ''):
        if var_name != '' and var_name in os.environ:
            return os.environ[var_name]
        return None

    #_ANS = get_secure_variable.__func__(var_name = '')

    ENV = ''
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = ''
    CSRF_KEY = ''
    MAIL_SUBJECT_PREFIX = 'Your company name'
    COMPANY_NAME = 'Your company name' # Change to your company name
    TRIAL_PERIOD_IN_DAYS = 14 # Change to your trial (in days, it's 2 weeks by default). Put 0 if no trial
    SAAS_API_KEY = get_secure_variable.__func__('saas_api_key') # Your api key for project-member
    SAAS_API_EMAIL = 'your_email_registered_in_project' # Your email as project-member
    # Mail sending settings (For privateemail by default)
    MAIL_SERVER = Config.get_secure_variable('mail_server')
    MAIL_PORT = Config.get_secure_variable('mail_port')
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = Config.get_secure_variable('mail_username')
    SECURITY_EMAIL_SENDER = Config.get_secure_variable('mail_username')
    MAIL_DEFAULT_SENDER = Config.get_secure_variable('mail_username')
    MAIL_PASSWORD = Config.get_secure_variable('mail_password')
    ADMIN_EMAIL = Config.get_secure_variable('admin_email')


class ProductionConfig(Config):
    ENV = 'prod'
    DEBUG = False
    SAAS_API_URL = 'https://www.saasidea.io'
    STRIPE_PUBLISHABLE_KEY = Config.get_secure_variable('STRIPE_PUBLISHABLE_KEY')
    STRIPE_SECRET_KEY = Config.get_secure_variable('STRIPE_SECRET_KEY')

    # The values below MUST store in the hosting config variables
    #SQLALCHEMY_DATABASE_URI
    #SECRET_KEY
    #SECRET_SALT

class DevelopmentConfig(Config):
    ENV = 'dev'
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ['db_url'] # Store it in the hosting config
    SECRET_KEY = Config.get_secure_variable('secret_key') # Store it in the hosting config
    SECRET_SALT = Config.get_secure_variable('secret_salt') # Store it in the hosting config
    TRIAL_PERIOD_IN_DAYS = 1 # Change it or remove it
    SAAS_API_URL = 'http://127.0.0.1:5000'
    STRIPE_PUBLISHABLE_KEY = Config.get_secure_variable('TEST_STRIPE_PUBLISHABLE_KEY')
    STRIPE_SECRET_KEY = Config.get_secure_variable('TEST_STRIPE_SECRET_KEY')


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
    