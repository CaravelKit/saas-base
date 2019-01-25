import sys
import stripe
from flask_restplus import Namespace, Resource, fields
from flask import jsonify, request, current_app
from flask_marshmallow import Marshmallow
from marshmallow import fields, validate
from flask_login import login_user, logout_user, login_required, current_user


account_api = Namespace('account', path='/api/account')

class AccountQuotaSchema(db_schema.Schema):
    class Meta:
        # Fields to expose
        fields = ('plan_name', 
            'user_project_number', 'user_project_members_number', 'api_calls_monthly_number', 
            'projects_left', 'user_project_members_left', 'api_calls_monthly_left')

account_quota_shema = AccountQuotaSchema()

@account_api.route('/quotas')
class AccountQuota(Resource):
    @login_required
    def get(self):
        acc_object = account_dal.get_account()
        return jsonify({
            'result': True,
            'quotas': account_quota_shema.dump(acc_object).data
        })

# This endpoint will hit when next subscription paid - by Stripe.
@account_api.route('/stripepaid')
class AccountSubscriptionPaidUpdate(Resource):
    def post(self):
        sig_header = request.headers.environ.get('HTTP_STRIPE_SIGNATURE')
        event = None
        interval = ''
        interval_count = 0
        try:
            event = stripe.Webhook.construct_event(
                request.get_data(), sig_header, current_app.config['STRIPE_ENDPOINT_SECRET']
            )
        except ValueError as e:
            # Invalid payload
            return 400
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return 400
        try:
            # Get plan data
            interval = account_api.payload['data']['object']['lines']['data'][0]['plan']['interval']
            interval_count = account_api.payload['data']['object']['lines']['data'][0]['plan']['interval_count']
        except Exception as e:
            print('ERROR: Could not get plan data...')

        # Update account data + create new account history data
        print('STRIPE update: ', account_api.payload['data']['object']['subscription'],
            account_api.payload['data']['object']['paid'], interval, interval_count)
        account_dal.update_account_paid(account_api.payload['data']['object']['subscription'], 
            account_api.payload['data']['object']['paid'], interval, interval_count, 
            account_api.payload['data']['object']['period_end'],
            account_api.payload['data']['object']['amount_paid'],
            account_api.payload['data']['object']['currency'])


        return 200
