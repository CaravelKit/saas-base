from flask import render_template, redirect, request, url_for, flash, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app import get_vendor

from app.blueprints.dashboard_blueprint import dashboard_blueprint

@dashboard_blueprint.before_app_request
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

@dashboard_blueprint.route('/dashboard', methods=['GET'], defaults={'path': None})
@dashboard_blueprint.route('/dashboard/<path:path>', methods=['GET'])
@login_required
def index_page(path):
    vendor = get_vendor()
    return render_template('dashboard.html', company_name=current_app.config.get('COMPANY_NAME'), vendor_pkey = vendor.get_public_key())


# API routes
@dashboard_blueprint.route('/api/userdata', methods=['GET'])
@login_required
def get_current_user_data():
    return jsonify({
        'result': True,
        'userdata': {
            'username': current_user.username,
            'subscribed': current_user.subscribed
        }
    })

@dashboard_blueprint.route('/api/userdata', methods=['POST'])
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