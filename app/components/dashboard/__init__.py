from flask import Blueprint

dashboard_component = Blueprint('dashboard', __name__, template_folder='templates')


def get_path_to_include():
    return 'a'

from . import routes