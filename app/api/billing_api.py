from flask import render_template, redirect, request, url_for, flash, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime as DateTime, timedelta as TimeDelta
from sqlalchemy import desc
import json

from app import db
from app.blueprints.billing_blueprint import billing_blueprint
from app.DAL.models.account_module import Account, AccountHistory
from app.DAL.constants.account_status import AccountStatus, ValidStatus
from app.DAL.constants.events import EventType
from app.utils.custom_login_required_api_decorator import login_required_for_api

from app import get_vendor


# API routes
@billing_blueprint.route('/api/billing/account', methods=['GET'])
@login_required_for_api
def get_user_account():
    # Determine if account is valid
    current_user.account.check_account_status()
    
    return jsonify({
        'result': True,
        'info': {
            'payment_method_info': current_user.account.payment_method_info,
            'payment_method_text': current_user.account.payment_method_text,
            'account_status_text': current_user.account.account_status_text,
            'account_status': current_user.account.account_status,
            'valid_status': current_user.account.valid_status,
            'trial_expiration': current_user.account.trial_expiration,
            'payment_expiration': current_user.account.payment_expiration,
            'plan_id': current_user.account.plan_id,
            'plan_name': current_user.account.plan_name,
            'vendor_name': current_user.account.vendor_name,
            'payment_method': current_user.account.payment_method
        }
    })

@billing_blueprint.route('/api/billing/history', methods=['GET'])
@login_required_for_api
def get_user_billing_history():
    data = current_user.account.account_history.order_by(desc(AccountHistory.date)).limit(100).all()
    history_data = json.loads(json.dumps([row.toDict() for row in data]))
    return jsonify({
        'result': True,
        'info': history_data
    })
    

@billing_blueprint.route('/api/billing/plan/list', methods=['GET'])
@login_required_for_api
def get_current_plans():
    vendor = get_vendor()
    plans = vendor.get_plans()
    return jsonify({
        'result': True,
        'plans': plans
    })

# Saves the method information for the current user
@billing_blueprint.route('/api/billing/paymentMethod', methods=['POST'])
@login_required_for_api
def save_payment_method():
    vendor = get_vendor() # to-do: make it based on request.json['vendor'] what is currently 'stripe' ??
    skey = vendor.get_secret_key()
    token = request.json['token']
    method_name = request.json['name']
    method_text = request.json['text']

    event = EventType.payment_method_selected if current_user.account.payment_method is None else EventType.payment_method_changed
    event_text = 'You selected ' if current_user.account.payment_method is None else 'You changed '

    payment_method_info = vendor.save_payment_method_info(current_user.email, **{'token': token})
    vendor_name = vendor.get_vendor_name() # what is primary - method or vendor? Probably method. So method should have this info.
    
    current_user.account.vendor_name = vendor_name
    current_user.account.payment_method = method_name
    current_user.account.payment_method_info = payment_method_info
    current_user.account.payment_method_text = method_text

    event_text = event_text + ' a payment method. ' + method_text
    current_user.account.create_history_event(event, event_text)

    db.session.add(current_user)
    db.session.commit()

    return jsonify({
        'result': True,
        'info': payment_method_info
    })

# Start subscription and buy it
@billing_blueprint.route('/api/billing/subscription', methods=['POST'])
@login_required_for_api
def start_subscription():
    vendor = get_vendor()
    skey = vendor.get_secret_key()
    
    event = EventType.subscription_paid
    if current_user.account.subscription_id != None:
        if request.json['plan_id'] == current_user.account.plan_id and current_user.account.account_status == 'paused':
            event = EventType.subscription_resumed

    subscription_data = vendor.create_subscription(request.json['plan_id'], 
        **{
            'payment_method_info': current_user.account.payment_method_info,
            'current_plan_id': current_user.account.plan_id,
            'current_subscription_id': current_user.account.subscription_id,
            'account_status': current_user.account.account_status
        }
    )
    if subscription_data['result']:
        next_payment = DateTime.fromtimestamp(subscription_data['period_end'])
        message_event = '{3}: Your payment succeed: {0} {1}.' if event == EventType.subscription_paid else 'Your subscription is resumed.'
        message_text = message_event + ' Your next payment will be on {2}.'
        message = message_text.format(subscription_data['amount'], subscription_data['currency'], next_payment.strftime('%d, %b %Y'),
            DateTime.now().strftime('%d, %b %Y'))
        current_user.account.create_history_event(event, message)

        # Update account data
        current_user.account.plan_id = request.json['plan_id']
        current_user.account.plan_name = request.json['plan_name']
        current_user.account.subscription_id = subscription_data['subscription_id']
        current_user.account.payment_expiration = next_payment
        current_user.account.account_status = AccountStatus.paid.value
        current_user.account.valid_status = ValidStatus.valid.value
        current_user.account.account_status_text = message
    else:
        message = 'Your payment failed: ' + subscription_data['message']
        current_user.account.create_history_event(EventType.subscription_failed, message)
        current_user.account.check_account_status() # We need to check and change if trial is expired already.

    db.session.add(current_user.account)
    db.session.commit()

    return jsonify({
        'result': subscription_data['result'],
        'account_status':current_user.account.account_status,
        'account_status_text': message,
        'payment_method_text': current_user.account.payment_method_text
    })

# Cancel/pause subscription
@billing_blueprint.route('/api/billing/subscription/cancelpause', methods=['POST'])
@login_required_for_api
def cancel_subscription():
    vendor = get_vendor()
    skey = vendor.get_secret_key()
    if current_user.account.plan_id == None or (current_user.account.account_status != AccountStatus.paid.value and
        current_user.account.account_status != AccountStatus.paused.value):
        return jsonify({
            'result': False,
            'message': 'You don\'t have any live subscription.'
        })
    cancel_result = vendor.cancel_subscription(current_user.account.subscription_id)
    pause_request = True if request.json != None and 'pause' in request.json else False
    if cancel_result['result'] == False:
        # to-do: log message
        pass
    else:
        if pause_request:
            current_user.account.account_status = AccountStatus.paused.value  
            current_user.account.account_status_text = 'The subscription was paused.'
        else:
            current_user.account.account_status = AccountStatus.cancelled.value  
            current_user.account.account_status_text = 'The subscription was cancelled.'
        if current_user.account.payment_expiration < DateTime.now():
            current_user.account.payment_expiration = None
            current_user.account.valid_status = ValidStatus.invalid.value 
            current_user.account.plan_name = ''
            current_user.account.plan_id = None
            current_user.account.subscription_id = ''
        else:   
            current_user.account.account_status_text += (' But you still have an access to the service until ' + 
                current_user.account.payment_expiration.strftime('%d, %b %Y') + '.')
        event = EventType.subscription_paused if pause_request else EventType.subscription_cancelled
        current_user.account.create_history_event(event, current_user.account.account_status_text)
        db.session.add(current_user.account)
        db.session.commit()

    return jsonify({
            'result': cancel_result['result'],
            'account_status':current_user.account.account_status,
            'account_status_text': current_user.account.account_status_text
        })