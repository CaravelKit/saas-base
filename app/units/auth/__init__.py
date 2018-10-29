from flask import Blueprint

auth_component = Blueprint('auth', __name__, template_folder='templates')

from . import routes