from datetime import datetime
import uuid
from flask import current_app, request, url_for
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import UUIDType
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.units.auth.models import role_module
from app.units.billing.models import account_module

#import hashlib
#from werkzeug.security import generate_password_hash, check_password_hash
#from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#from flask_login import UserMixin, AnonymousUserMixin
#from app.exceptions import ValidationError
from app import login_manager
from app import db
from app.units.billing.models.account_module import Account


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(UUID(as_uuid=True),
        primary_key=True, default=lambda: uuid.uuid4().hex)
    email = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('role.id'))
    confirmed = db.Column(db.Boolean, default=False)
    subscribed = db.Column(db.Boolean, default=False)
    account_id = db.Column(UUID(as_uuid=True), db.ForeignKey('account.id'))
    account = db.relationship('Account', back_populates='user')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ADMIN_EMAIL']:
                self.role = role_module.Role.query.filter_by(name='Admin').first()
            else:
                default_role = role_module.Role.query.filter_by(is_default=True).first()
                self.role = default_role
        if self.account == None:
            self.account = Account()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(uuid.UUID(user_id))

    def set_password(self, password):
        salted_pwd = (password + self.email + current_app.config['SECRET_SALT']).encode('utf-8')
        self.password_hash = generate_password_hash(salted_pwd).decode('utf-8')

    def verify_password(self, password):
        salted_pwd = (password + self.email + current_app.config['SECRET_SALT']).encode('utf-8')
        return check_password_hash(self.password_hash, salted_pwd)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id.__str__()}).decode('utf-8')
    
    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id.__str__()}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id.__str__():
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
