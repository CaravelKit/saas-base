import os
from flask import current_app
def init(app):
    app.jinja_env.filters['generate_url_from_title'] = generate_url_from_title
    return

def generate_url_from_title(title):
    return title.replace(' ', '_').lower()
