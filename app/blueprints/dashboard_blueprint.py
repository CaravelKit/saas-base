from flask import Blueprint

dashboard_blueprint = Blueprint('dashboard', __name__, template_folder='templates')

from app.api import dashboard_api