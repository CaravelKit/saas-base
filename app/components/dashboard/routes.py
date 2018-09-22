from flask import render_template, redirect, request, url_for, flash, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app import db

from . import dashboard_component

@dashboard_component.before_app_request
def before_request():
    if request.endpoint \
        and request.blueprint != 'auth' \
        and request.endpoint != 'static':
            url_redirect = ''
            if current_user.is_authenticated:
                if not current_user.confirmed:
                    url_redirect = url_for('auth.confirm_email', userid = str(current_user.id))
            else:
                url_redirect = url_for('auth.login_page')
            if request.path.startswith('/api'):
                # This is for API calls
                if url_redirect:
                    return jsonify({'result': False, 'redirect': url_redirect})
            else:
                # This is for pages calls
                if url_redirect:
                    return redirect(url_redirect)

@dashboard_component.route('/dashboard', methods=['GET'], defaults={'path': None})
@dashboard_component.route('/dashboard/<path:path>', methods=['GET'])
@login_required
def index_page(path):
    return render_template('dashboard.html', company_name=current_app.config.get('COMPANY_NAME'))


# API routes
@dashboard_component.route('/api/userdata', methods=['GET'])
@login_required
def get_current_user_data():
    return jsonify({
        'result': True,
        'userdata': {
            'username': current_user.username,
            'subscribed': current_user.subscribed
        }
    })

@dashboard_component.route('/api/userdata', methods=['POST'])
@login_required
def update_current_user_data():
    user_data = request.get_json();
    current_user.username = user_data['username']
    current_user.subscribed = user_data['subscribed']
    db.session.add(current_user)
    db.session.commit()
    return jsonify({
        'result': True,
    })