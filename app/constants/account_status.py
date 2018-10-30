from enum import Enum

class ValidStatus(Enum):
    invalid = 'invalid' # User didn't select a trial, didn't paid, or cancelled subscription
    valid = 'valid'

class AccountStatus(Enum):
    undefined = ''
    trial = 'trial' # User started trial
    paid = 'paid' # User started subscription and paid
    paused = 'paused' # User stopped next payment until he decides to activate it again
    cancelled = 'cancelled'

class PaymentMethodStatus(Enum):
    empty = 'empty'
    entered = 'entered'

class PlanStatus(Enum):
    empty = 'empty'
    entered = 'entered'
