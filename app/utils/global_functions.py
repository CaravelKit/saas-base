import os
from flask import current_app
def init(app):
    app.jinja_env.globals.update(get_abs_path=get_abs_path) 
    return

def get_abs_path(relative_path):
    return os.path.abspath(os.path.join(current_app.root_path, relative_path))