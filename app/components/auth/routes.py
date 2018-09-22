import uuid
from flask import render_template, redirect, request, url_for, flash, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import user_module
from app.utils.email import send_email
from .forms import LoginForm, RegistrationForm, ChangePasswordForm,\
    PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm

import app.utils.error_handler as error_handler

from . import auth_component


@auth_component.before_app_request
def before_request():
    # Add here a main page (landing) if you have it.
    if request.endpoint \
        and request.blueprint != 'auth' \
        and request.endpoint != 'static':
            if current_user.is_authenticated:
                if not current_user.confirmed:
                    return redirect(url_for('auth.confirm_email', userid = str(current_user.id)))
            else:
                return redirect(url_for('auth.login_page'))



# This code is to show you how to redirect to error page - if it's not 404 or 500, but just something went wrong.
@auth_component.route('/testerror', methods=['GET'])
def testerror():
    return error_handler.app_error('Some unknown error', 'some error text')

@auth_component.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html', company_name=current_app.config['COMPANY_NAME'])

@auth_component.route('/login', methods=['POST'])
def login_api():
    form = LoginForm()
    if form.validate_on_submit():
        user = user_module.User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            dashboard_url = url_for('dashboard.index_page')
            return jsonify({'result': True, 'redirect': dashboard_url})
        return jsonify({'result': False, 'errors': ['Invalid username or password.']})
    else:
        return jsonify({'result': False, 'errors': ['Invalid username or password.']})


@auth_component.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login_page'))


@auth_component.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html', company_name=current_app.config['COMPANY_NAME'])

@auth_component.route('/register', methods=['POST'])
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
        send_email(user.email, 'Please confirm Your Email', 'confirmation', user=user, token=token, company_name=current_app.config['COMPANY_NAME'])
        confirm_email = url_for('auth.confirm_email', userid = str(user.id))
        return jsonify({'result': True, 'redirect': confirm_email})
    else:
        #render_template('register.html', form=form)
        return jsonify({'result': False, 'errors': form.errors})

# This page is open only after registration by the client code itself, or in a case when unconfirmed user tries to login
@auth_component.route('/confirmemail/<userid>', methods=['GET'])
def confirm_email(userid):
    user = user_module.User.query.filter_by(id=uuid.UUID(userid).hex).first()
    if user:  
        flash('We\'ve sent you the confirmation email, please open it and click on the confirmation link.')      
        return render_template("confirmemail.html", userid = userid, company_name=current_app.config['COMPANY_NAME'])
    return error_handler.app_error('User identification error', 'Sorry but user not found. Please login or register again.')

@auth_component.route('/confirm/<token>/<userid>', methods=['GET'])
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

@auth_component.route('/confirmed')
def confirmed():
    return render_template('confirmed.html', company_name=current_app.config['COMPANY_NAME'])

@auth_component.route('/resendconfirm/<userid>')
def resend_confirmation(userid):
    user = user_module.User.query.filter_by(id=uuid.UUID(userid).hex).first()
    if user:
        token = user.generate_confirmation_token()
        send_email(user.email, 'Please confirm Your Email', 'confirmation', user=user, token=token, company_name=current_app.config['COMPANY_NAME'])
        flash('We\'ve resent you the confirmation email. Please open your mail and click the link inside.')
        return render_template("confirmemail.html", userid = userid, company_name=current_app.config['COMPANY_NAME'])
    return error_handler.app_error('User identification error', 'Sorry but user not found. Please login or register again.')