from flask import Blueprint

billing_blueprint = Blueprint('billing', __name__)

from app.api import billing_api