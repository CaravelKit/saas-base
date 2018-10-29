from flask import Blueprint

billing_component = Blueprint('billing', __name__)

from .api import routes