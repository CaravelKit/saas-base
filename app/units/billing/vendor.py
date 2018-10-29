from sys import exc_info
from abc import ABCMeta, abstractmethod
from app.utils.global_functions import get_secure_variable
import stripe

class Vendor_base:

    keys = None

    @abstractmethod
    def get_vendor_name(self):
        pass

    @abstractmethod
    def init_keys(self):
        pass

    @abstractmethod
    def get_plans(self):
        pass
    
    @abstractmethod
    def get_default_trial_plan_id(self):
        pass

    @abstractmethod
    def get_public_key(self):
        pass

    @abstractmethod
    def get_secret_key(self):
        pass

    @abstractmethod
    def save_payment_method_info(self, user_email, **kwargs):
        pass

    @abstractmethod
    def create_subscription(self, plan_id, **kwargs):
        pass

    @abstractmethod
    def cancel_subscription(self, subscription_id):
        pass

    @abstractmethod
    def pause_subscription(self, subscription_id):
        pass

    @abstractmethod
    def resume_subscription(self, plan_id, **kwargs):
        pass
    

class Vendor_Stripe(Vendor_base):

    def get_vendor_name(self):
        return 'stripe'
    
    def init_keys(self):
        env = get_secure_variable('env')
        self.keys = {
            'publishable_key': get_secure_variable('STRIPE_PUBLISHABLE_KEY') if env == 'prod' else get_secure_variable('TEST_STRIPE_PUBLISHABLE_KEY'),
            'secret_key': get_secure_variable('STRIPE_SECRET_KEY') if env == 'prod' else get_secure_variable('TEST_STRIPE_SECRET_KEY'), 
        }
        stripe.api_key = self.keys['secret_key']

    def map_plan_data(self, plan):
        new_plan = {}
        new_plan['id'] = plan['id']
        new_plan['name'] = plan['nickname']
        new_plan['active'] = plan['active']
        new_plan['price'] = "{:0.0f}".format(plan['amount']/100)
        new_plan['currency'] = plan['currency'].upper()
        new_plan['interval'] = plan['interval']
        new_plan['interval_count'] = plan['interval_count']
        if plan['metadata'] is not None:
            new_plan['features'] = []
            features = {}
            if 'description' in plan['metadata']:
                new_plan['description'] = plan['metadata']['description']
            for key in dict(plan['metadata']):
                if key.startswith('feature'):
                    parts = key.split(':')
                    if len(parts) == 2:
                        if parts[1].isnumeric:
                            features[int(parts[1])] = plan['metadata'][key]
                            
            features = dict(sorted(features.items()))
            new_plan['features'] = list(features.values())
            #new_plan['features'].insert(int(parts[1]), plan['metadata'][key])
            # Deterime if this plan is a default for a trial
            if 'default' in plan['metadata']:
                if plan['metadata']['default'] == 'trial':
                    new_plan['default'] = 'trial'
        return new_plan

    def get_plans(self):
        raw_plans = stripe.Plan.list()
        mapped_plans = list(map(self.map_plan_data, raw_plans.data))
        return mapped_plans
    
    def get_default_trial_plan_id(self):
        plans_list = stripe.Plan.list()
        plan_default_id = None
        for plan in plans_list.data:
            if plan['metadata'] is not None:
                if 'default' in plan['metadata']:
                    if plan['metadata']['default'] == 'trial':
                        plan_default_id = plan['id']
                        break 
        if plan_default_id is None:
            if len(plans_list.data) > 0:
                plan_default_id = plans_list.data[0]['id']
        return plan_default_id

    def get_public_key(self):
        return self.keys['publishable_key']

    def get_secret_key(self):
        return self.keys['secret_key']

    def save_payment_method_info(self, user_email, **kwargs):
        customer = stripe.Customer.create(
            email = user_email,
            source = kwargs['token']
        )
        return customer.id if customer != None else None

    def create_subscription(self, plan_id, **kwargs):
        subscription = None
        customer_id = kwargs['payment_method_info']
        try:
            # Firstly cancel any existing subscription

            if kwargs['current_subscription_id'] != None:
                subscription = stripe.Subscription.retrieve(kwargs['current_subscription_id'])
                if plan_id == kwargs['current_plan_id'] and kwargs['account_status'] == 'paused':
                    # Just reactivate
                    subscription.cancel_at_period_end = False
                    subscription.save()
                else:
                    # Delete an old subscription and create a new one
                    if (subscription != None):
                        subscription.delete()
                    subscription = stripe.Subscription.create(
                        customer = customer_id,
                        items = [
                            {
                                'plan': plan_id,
                            }
                        ]
                    )
        except:
            # to-do: log exception sys.exc_info()[0]
            print(exc_info()[0])
        if subscription is None:
            return {
                'result': False,
                'message': 'Something went wrong and we could not charge you. Please make sure you provided valid payment information.'
            }

        return {
            'result': True,
            'subscription_id': subscription.id,
            'amount': "{:.2f}".format(subscription['items']['data'][0]['plan']['amount'] / 100),
            'currency': subscription['items']['data'][0]['plan']['currency'].upper(),
            'period_end': subscription['current_period_end']
        }

    def cancel_subscription(self, subscription_id):
        result = True
        message = ''
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            subscription.cancel_at_period_end = True
            subscription.save() # or use subscription.delete()
        except:
            # to-do: log exception sys.exc_info()[0]
            print(exc_info()[0])
            result = False
        return {
            'result': result
        }

    def resume_subscription(self, plan_id, **kwargs):
        return self.create_subscription(self, plan_id, **kwargs)