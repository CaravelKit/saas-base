from flask import Blueprint

dashboard_component = Blueprint('dashboard', __name__, template_folder='templates')

from . import routes