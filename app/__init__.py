import sys, os
from pathlib import Path

from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_alembic import Alembic

from config import ConfigHelper

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()
alembic = Alembic()
app_path = ''
vendor = None

def get_vendor():
    return vendor

def create_app():
    
    app = Flask(__name__) 
    redefine_delimiters(app)
    dist_folder = os.path.abspath(os.path.join(app.root_path,"../static"))
    app.static_folder = dist_folder
    app.static_url_path='/static'
    app_path = app.root_path
    app.url_map.strict_slashes = False
    app.config.from_object(ConfigHelper.set_config(sys.argv))
    initialize_libraries(app)
    init_filters(app)
    init_global_functions(app)
    register_blueprints(app)
    register_error_handlers(app)
    init_payment_vendor(app)
    return app

def redefine_delimiters(app):
    jinja_options = app.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='{%',
        block_end_string='%}',
        variable_start_string='${',
        variable_end_string='}',
        comment_start_string='{#',
        comment_end_string='#}',
    ))
    app.jinja_options = jinja_options

def init_app_path(path):
    global app_path
    app_path = path

def init_db(option, app):
    import app.utils.dbscaffold as dbscaffold
    dbscaffold.reinit_db(option)

def init_payment_vendor(app):
    global vendor
    from app.DAL.services.vendor import Vendor_Stripe, Vendor_base # to-do it dynamically
    vendor = Vendor_Stripe(app) # to-do: vendor is selected based on config
    vendor.init_keys()

def initialize_libraries(app):
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    alembic.init_app(app)

def register_blueprints(app):
    from app.blueprints.auth_blueprint import auth_blueprint
    from app.blueprints.dashboard_blueprint import dashboard_blueprint
    from app.blueprints.billing_blueprint import billing_blueprint

    blueprints = [auth_blueprint, dashboard_blueprint, billing_blueprint] # Add a new blueprint here # to-do: automate it
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    

def get_path_to_include(relative_path):
    return os.path.abspath(os.path.join(app_path, relative_path))

def init_filters(app):
    from app.utils import filters
    filters.init(app)

def init_global_functions(app):
    from app.utils import global_functions
    global_functions.init(app)

def register_error_handlers(app):
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, page_server_error)

def page_not_found(e):
    from app.utils import error_handler
    return error_handler.app_error(error_title='PAGE NOT FOUND', error_text='The page you asked for not found...'), 404

def page_server_error(e):
    from app.utils import error_handler
    return error_handler.app_error(error_title='CRITICAL ERROR', error_text='Something went wrong... please try again.'), 500

