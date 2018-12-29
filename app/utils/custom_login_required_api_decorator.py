from flask_login.config import EXEMPT_METHODS
from functools import wraps
from flask import request, current_app
from flask_login import current_user
from flask import jsonify

def login_required_for_api(func):
    @wraps(func)
    def custom_decorated_view_for_api(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return jsonify({
                'result': False,
                'errors': ['You are not authorized. Please refresh the page and try again.']
            })
        return func(*args, **kwargs)
    return custom_decorated_view_for_api