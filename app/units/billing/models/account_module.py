from datetime import datetime
import uuid
from flask import current_app, request, url_for
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import UUIDType
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime as DateTime, timedelta as TimeDelta

from app.constants.account_status import AccountStatus, ValidStatus
from .account_history_module import AccountHistory
from app.constants.events import EventType
from app import login_manager
from app import db
from app import get_vendor


class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4().hex)
    user = db.relationship('User', back_populates='account')
    account_history = db.relationship("AccountHistory", backref='account', lazy='dynamic')
    
    # payment information
    payment_method = db.Column(db.String()) # May be: 'card', 'paypal' or anything else
    payment_method_info = db.Column(db.String()) # Vendor - specific information
    payment_method_text = db.Column(db.String(150)) # Any text information for user that will be shown as current payment info
    account_status_text = db.Column(db.String(150)) # Ane text information describing the current account status (trial, paid, paused etc.)
    vendor_name = db.Column(db.String(64))
    subscription_id = db.Column(db.String(128))
    plan_id = db.Column(db.String(64))
    plan_name = db.Column(db.String(128))
    api_key = db.Column(db.String(128)) # API key generated automatically by API

    # Below is current actual information
    # If account is valid that is has access to some plan
    valid_status = db.Column(db.String(32)) # It's string because alembic cannot update Enums

    # Current status: trial, paid, or paused
    account_status = db.Column(db.String(32))

    # Additional fields
    trial_expiration = db.Column(db.DateTime(), nullable=True)
    payment_expiration = db.Column(db.DateTime(), nullable=True)



    def __init__(self):
        self.valid_status = ValidStatus.invalid.value # It's invalid by default
        self.start_trial()
        #self.account_status = AccountStatus.trial.value # when user signs up, he gets the trial automatically
        #trial_days = current_app.config['TRIAL_PERIOD_IN_DAYS']
        #self.trial_expiration = DateTime.today() + TimeDelta(days = trial_days)

    # Checks if account is active or not, change fields and the current status
    def check_account_status(self):#trial_status, purchase_status, payment_method_status, plan_status):
        current_valid_status = ValidStatus.valid
        current_account_status = AccountStatus(self.account_status)
        if self.account_status == AccountStatus.trial.value:
            # Check if the trial's not expired yet
            if DateTime.today() > self.trial_expiration:
                current_valid_status = ValidStatus.invalid
                current_account_status = AccountStatus.undefined
                self.account_status_text = 'Your trial is expired. Please buy a subscription to continue using the service.'
                self.trial_expiration = None
                self.plan_id = ''
        else:
            # Trial is inactive or not started yet. Check payment status.
            if (self.account_status == AccountStatus.cancelled.value or 
                self.account_status == AccountStatus.paused.value or 
                self.account_status == AccountStatus.undefined.value):
                current_valid_status = ValidStatus.invalid
            else:        
                # Account status is paid, check if it's still valid
                if self.payment_expiration != None and DateTime.now() > self.payment_expiration:
                    current_valid_status = ValidStatus.invalid

        if current_valid_status.value != self.valid_status or current_account_status.value != self.account_status:
            self.valid_status = current_valid_status.value
            self.account_status = current_account_status.value
            db.session.add(self)
            db.session.commit()

    def create_history_event(self, event: EventType, comment: str):
        new_event = AccountHistory()
        new_event.account_id = self.id
        new_event.date = datetime.now()
        new_event.event = event.value
        new_event.comment = comment
        db.session.add(new_event)

    def start_trial(self):
        vendor = get_vendor()
        self.plan_id = vendor.get_default_trial_plan_id()
        trial_days = current_app.config['TRIAL_PERIOD_IN_DAYS']
        self.trial_expiration = DateTime.today() + TimeDelta(days = trial_days)
        self.account_status = AccountStatus.trial.value
        str_valid_time = self.trial_expiration.strftime('%d, %b %Y %H:%M')
        self.account_status_text = ('Your trial is activated and valid till ' + 
            str_valid_time)
        db.session.add(self)
        db.session.flush()
        account_event = self.create_history_event(EventType.trial_started, 'Started a trial, expiration date is ' + str_valid_time)

    