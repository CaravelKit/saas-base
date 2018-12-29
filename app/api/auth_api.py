import uuid
from urllib import parse
from flask import render_template, redirect, request, url_for, flash, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.DAL.models import user_module
from app.DAL.models import account_module
from app.utils.email import send_email
from app.DAL.services.auth_forms import LoginForm, RegistrationForm, ChangePasswordForm,\
    PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm

import app.utils.error_handler as error_handler
from app.blueprints.auth_blueprint import auth_blueprint


# This code is to show you how to redirect to error page - if it's not 404 or 500, but just something went wrong.
@auth_blueprint.route('/testerror', methods=['GET'])
def testerror():
    return error_handler.app_error('Some unknown error', 'some error text')

@auth_blueprint.route('/login', methods=['GET'])
def login_page():
    if current_user.is_authenticated:
        if not current_user.confirmed:
            return redirect(url_for('auth.confirm_email', userid = str(current_user.id)))
    return render_template('/auth/login.html', company_name=current_app.config['COMPANY_NAME'])

@auth_blueprint.route('/login', methods=['POST'])
def login_api():
    form = LoginForm()
    if form.validate_on_submit():
        user = user_module.User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            prev_url = ''
            if request.referrer:
                prev_query = parse.urlparse(request.referrer).query
                if prev_query and parse.parse_qs(prev_query).get('next'):
                    prev_url = parse.parse_qs(prev_query).get('next')[0]
            redirect_url = prev_url or url_for('dashboard.index_page')
            return jsonify({'result': True, 'redirect': redirect_url})
        return jsonify({'result': False, 'errors': ['Invalid username or password.']})
    else:
        return jsonify({'result': False, 'errors': ['Invalid username or password.']})


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login_page'))


@auth_blueprint.route('/register', methods=['GET'])
def register_page():
    return render_template('/auth/register.html', company_name=current_app.config['COMPANY_NAME'])

@auth_blueprint.route('/register', methods=['POST'])
def register_api():
    form = RegistrationForm()
    if form.validate():
        user = user_module.User(email = form.email.data,
                    username = form.username.data,
                    confirmed = False)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Please confirm Your Email', '/non_auth/confirmation', user=user, token=token, company_name=current_app.config['COMPANY_NAME'])
        confirm_email = url_for('auth.confirm_email', userid = str(user.id))
        return jsonify({'result': True, 'redirect': confirm_email})
    else:
        return jsonify({'result': False, 'errors': form.errors})

# This page is open only after registration by the client code itself, or in a case when unconfirmed user tries to login
@auth_blueprint.route('/confirmemail/<userid>', methods=['GET'])
def confirm_email(userid):
    user = user_module.User.query.filter_by(id=uuid.UUID(userid).hex).first()
    if user:  
        flash('We\'ve sent you the confirmation email, please open it and click on the confirmation link.')      
        return render_template("/auth/confirmemail.html", userid = userid, company_name=current_app.config['COMPANY_NAME'])
    return error_handler.app_error('User identification error', 'Sorry but user not found. Please login or register again.')

@auth_blueprint.route('/confirm/<token>/<userid>', methods=['GET'])
def confirm(token, userid):
    user = user_module.User.query.filter_by(id=uuid.UUID(userid).hex).first()
    if user:  
        if not user.confirmed:          
            if user.confirm(token):
                db.session.commit()
                # User is confirmed, but we have to logout to make sure that THIS exact user will login then.
        logout_user()
        return redirect(url_for('auth.confirmed'))
    else:
        return error_handler.app_error('User identification error', 'Sorry but user not found. Please login or register again.')

@auth_blueprint.route('/confirmed')
def confirmed():
    return render_template('/auth/confirmed.html', company_name=current_app.config['COMPANY_NAME'])

@auth_blueprint.route('/resendconfirm/<userid>')
def resend_confirmation(userid):
    user = user_module.User.query.filter_by(id=uuid.UUID(userid).hex).first()
    if user:
        token = user.generate_confirmation_token()
        send_email(user.email, 'Please confirm Your Email', '/non_auth/confirmation', user=user, token=token, company_name=current_app.config['COMPANY_NAME'])
        flash('We\'ve resent you the confirmation email. Please open your mail and click the link inside.')
        return render_template("/auth/confirmemail.html", userid = userid, company_name=current_app.config['COMPANY_NAME'])
    return error_handler.app_error('User identification error', 'Sorry but user not found. Please login or register again.')