import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    @staticmethod
    def get_secure_variable(var_name = '', default_value = None):
        if var_name != '' and var_name in os.environ:
            return os.environ[var_name]
        if default_value is not None:
            return default_value

    #_ANS = get_secure_variable.__func__(var_name = '')

    ENV = ''
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = ''
    CSRF_KEY = ''
    MAIL_SUBJECT_PREFIX = 'Your company name'
    COMPANY_NAME = 'Your company name' # Change to your company name
    TRIAL_PERIOD_IN_DAYS = 14 # Change to your trial (in days, it's 2 weeks by default). Put 0 if no trial
    SAAS_API_KEY = os.environ.get('saas_api_key') # Your api key for project-member
    SAAS_API_EMAIL = 'your_email_registered_in_project' # Your email as project-member
    # Mail sending settings (For privateemail by default)
    MAIL_SERVER = os.environ.get('mail_server')
    MAIL_PORT = os.environ.get('mail_port')
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get('mail_username')
    SECURITY_EMAIL_SENDER = os.environ.get('mail_username')
    MAIL_DEFAULT_SENDER = os.environ.get('mail_username')
    MAIL_PASSWORD = os.environ.get('mail_password')
    ADMIN_EMAIL = os.environ.get('admin_email')
    STRIPE_ENDPOINT_SECRET = os.environ.get('stripe_endpoint_secret')


class ProductionConfig(Config):
    ENV = 'prod'
    DEBUG = False
    SAAS_API_URL = 'https://www.saasidea.io'
    STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')

    # The values below MUST store in the hosting config variables
    #SQLALCHEMY_DATABASE_URI
    #SECRET_KEY
    #SECRET_SALT

class DevelopmentConfig(Config):
    ENV = 'dev'
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('db_url') # Store it in the hosting config
    SECRET_KEY = os.environ.get('secret_key') # Store it in the hosting config
    SECRET_SALT = os.environ.get('secret_salt') # Store it in the hosting config
    TRIAL_PERIOD_IN_DAYS = 1 # Change it or remove it
    SAAS_API_URL = 'http://127.0.0.1:5000'
    STRIPE_PUBLISHABLE_KEY = os.environ.get('TEST_STRIPE_PUBLISHABLE_KEY')
    STRIPE_SECRET_KEY = os.environ.get('TEST_STRIPE_SECRET_KEY')
    SAAS_API_KEY = os.environ.get('saas_api_key')
    SAAS_API_EMAIL = os.environ.get('saas_api_email')

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
    