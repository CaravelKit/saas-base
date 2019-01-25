import uuid
from datetime import datetime
from dateutil.relativedelta import *
from ast import literal_eval
from sqlalchemy import func
from sqlalchemy import text
from flask_login import current_user
from app import db
from app.utils.global_functions import get_config_var
from app.DAL.models.account_module import Account
from app.DAL.constants.events import EventType


# to-do: paging
def get_account():
    return Account.query.filter_by(id = current_user.account_id).first()

def update_account_paid(subscription_id, paid, interval, interval_count, period_end, amount, currency):
    if subscription_id is None or subscription_id == '':
        return {
            'result': False
        }
    try:
        account = Account.query.filter_by(subscription_id = subscription_id).first()
        # It may be None when account is just created but didn't saved in the database
        if account is not None:
            print('Account ID:', account.id)
            if paid:
                # Update any data you want
                result = {'result': True}
                # Create new account history event
                next_payment = datetime.fromtimestamp(period_end)
                message_event = '{3}: Your payment succeed: {0} {1}.'
                message_text = message_event + ' Your next payment will be on {2}.'
                message = message_text.format(amount, currency, next_payment.strftime('%d, %b %Y'),
                    datetime.now().strftime('%d, %b %Y'))
                account.create_history_event(EventType.subscription_paid, message)

                db.session.commit()               
                return result
        else:
            print('Account is None')
    except Exception as ex:
        # to-do: log
        print(ex)
        return {
            'result': False
        }