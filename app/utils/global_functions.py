import os, sys
from flask import current_app
from google.cloud import datastore

def init(app):
    app.jinja_env.globals.update(get_abs_path=get_abs_path) 
    return

def get_abs_path(relative_path):
    return os.path.abspath(os.path.join(current_app.root_path, relative_path))


google_datastore_client = None
def get_secure_variable(var_name):
    # 1) check env variable
    if var_name in os.environ:
        return os.environ[var_name]
    # 2) Get var from the Google datastore 
    try:
        google_datastore_client = datastore.Client() if google_datastore_client is None else google_datastore_client
        key = google_datastore_client.key('Settings', 'env_var')
        val = google_datastore_client.get(key)
        if var_name in val:
            return val[var_name]
    except:
        pass
    return None