from flask import Blueprint

main_component = Blueprint('main', __name__, template_folder='templates')

from . import routes