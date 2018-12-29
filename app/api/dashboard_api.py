from flask import render_template, redirect, request, url_for, flash, jsonify, current_app
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app import get_vendor
from app.blueprints.dashboard_blueprint import dashboard_blueprint
from app.utils.custom_login_required_api_decorator import login_required_for_api


@dashboard_blueprint.route('/dashboard', methods=['GET'], defaults={'path': None})
@dashboard_blueprint.route('/dashboard/<path:path>', methods=['GET'])
@login_required
def index_page(path):
    vendor = get_vendor()
    return render_template('dashboard.html', company_name=current_app.config.get('COMPANY_NAME'), vendor_pkey = vendor.get_public_key())


# API routes
@dashboard_blueprint.route('/api/userdata', methods=['GET'])
@login_required_for_api
def get_current_user_data():
    return jsonify({
        'result': True,
        'userdata': {
            'username': current_user.username,
            'subscribed': current_user.subscribed
        }
    })

@dashboard_blueprint.route('/api/userdata', methods=['POST'])
@login_required_for_api
def update_current_user_data():
    user_data = request.get_json();
    current_user.username = user_data['username']
    current_user.subscribed = user_data['subscribed']
    db.session.add(current_user)
    db.session.commit()
    return jsonify({
        'result': True,
    })