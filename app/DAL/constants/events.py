from enum import Enum

class EventType(Enum):
    # Payment
    trial_started = 'trial_start'
    trial_ended = 'trial_end'
    plan_selected = 'plan_sel'
    plan_changed = 'plan_chan'
    payment_method_selected = 'pay_method_sel'
    payment_method_changed = 'pay_method_chan'
    subscription_paid = 'subscription_paid'
    subscription_failed = 'subscription_failed'
    subscription_cancelled = 'subscription_cancelled'
    subscription_paused = 'subscription_paused'
    subscription_resumed = 'subscription_resumed'

def get_text_event(event: EventType):
    dic = {
        EventType.trial_started: 'Trial pediod started',
        EventType.trial_ended: 'Trial period ended',
        EventType.plan_selected : 'Plan selected',
        EventType.plan_changed : 'Plan changed',
        EventType.payment_method_selected : 'Payment method selected',
        EventType.payment_method_changed : 'Payment method changed',
        EventType.subscription_paid : 'Subscription paid',
        EventType.subscription_failed : 'Subscription payment failed',
        EventType.subscription_cancelled : 'Subscription cancelled',
        EventType.subscription_paused : 'Subscription paused',
        EventType.subscription_resumed : 'Subscription resumed'
    }
    return dic[event]