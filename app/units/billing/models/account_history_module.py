from datetime import datetime
import uuid
from flask import current_app, request, url_for
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import UUIDType
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app import login_manager
from app import db
from . import account_module
from app.constants.events import EventType, get_text_event


class AccountHistory(db.Model):
    __tablename__ = 'account_history'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4().hex)
    account_id = db.Column(UUID(as_uuid=True), db.ForeignKey('account.id'))
    date = db.Column(db.DateTime(), nullable=True)
    event = db.Column(db.String(32), nullable=True) # Some text representation of event
    comment = db.Column(db.String(128)) # Text comment

    def toDict(self):
        def read_field(field_value, field_name):
            if (field_name == 'event'):
                return get_text_event(EventType(field_value))
            res = str(field_value)
            return res
        return {c.name: read_field(getattr(self, c.name), c.name) for c in self.__table__.columns}#{ c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
    