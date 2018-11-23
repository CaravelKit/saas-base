from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import UUIDType
import uuid

#import hashlib
#from werkzeug.security import generate_password_hash, check_password_hash
#from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#from flask import current_app, request, url_for
#from flask_login import UserMixin, AnonymousUserMixin
#from app.exceptions import ValidationError
#from . import db, login_manager
from app import db


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(UUID(as_uuid=True),
        primary_key=True, default=lambda: uuid.uuid4().hex)
    is_default = db.Column(db.Boolean, default=False, server_default='f')
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
