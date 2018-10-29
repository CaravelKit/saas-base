<template>
    <div>
        <h5>Select a payment method</h5>
        <h6>Use this form if you want to change or create your payment method</h6>
        <div class="alert alert-info">
            <strong>Important note! </strong>We don't store any credit card or other sensitive information. All data 
            is securely stored on our Vendor's servers (see vendor's name in the list of payment methods below).
        </div>
        <div class="billing-price">
            <div class="plan-block method-block" v-for="(method, index) in paymentMethods">
                <div class="row" v-show="method.name=='card'">
                    <div class="col-sm-12 col-md-12 col-lg-7">
                        <h5>
                            <img :src="'/static/media/cc.png'" />
                            <img :src="'/static/media/powered_by_' + method.vendor_name + '.png'" class="float-right" v-if="method.vendor_name" />
                        </h5>
                        <form id="payment-form">
                            <div>
                                <label for="card-element">
                                    Enter you credit or debit card data
                                </label>
                                <div id="card-element" class="form-control">
                                <!-- A Stripe Element will be inserted here. -->
                                </div>
                            </div>
                        </form>
                        <div v-show="accountInfo.payment_method == method.name" class="info-small-block">
                            {{accountInfo.payment_method_text}}
                        </div>
                    </div>
                    <div class="col-sm-12 col-md-12 col-lg-5 select-method-block">
                        <div v-show="method.name == $store.state.accountInfo.payment_method">
                            <i class="fas fa-check icon-green"></i><span>Selected method</span>
                        </div>
                        <button class="btn btn-primary" 
                            @click="selectMethodAndSave(index)">{{buttonText(method.name)}}
                        </button>
                    </div>
                </div>
                <div class="row" v-show="method.name=='paypal'">
                    <div class="col-sm-12 col-md-12 col-lg-7">
                        <h5><img :src="'/static/media/paypal.png'" /></h5>
                        <span>Coming soon!</span>
                    </div>
                </div>
                <br>
                <div class="row">
                    <div class="col-12">
                        <div id="card-errors" role="alert" class="alert alert-danger" v-show="method.error">{{method.error}}</div>
                        <div role="alert" class="alert alert-success" v-show="method.success">{{method.success}}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

import { httpService } from '@app/units/common/httpService.js'; 
import _ from 'lodash';

export default {
    name: 'PaymentMethod',
    data: function(){
        return {
            paymentMethods: [
                {
                    name: 'card',
                    vendor_name: 'stripe',
                    data: {
                        stripeApp: null,
                        elements: null,
                        card: undefined
                    }, 
                    selected: false,
                    error: '',
                    success: ''
                },
                {
                    name: 'paypal'
                }
            ]
        };
    },
    mounted: function(){
        // to-do: init other methods, currently only Stripe is initialized
        var cardMethod = _.find(this.paymentMethods, {name: 'card'});
        if (cardMethod){
            cardMethod.data.stripeApp = Stripe(window.vendor_pkey);  // to-do: vendor may be different depending on the config
            cardMethod.data.elements = cardMethod.data.stripeApp.elements();
            cardMethod.data.card = cardMethod.data.elements.create('card', {hidePostalCode: true});
            cardMethod.data.card.mount('#card-element');
        }
    },
    computed: {
        paymentInfo() {
            return this.$store.state.billingInfo;
        },
        accountInfo() {
            return this.$store.state.accountInfo;
        }
    },
    methods: {
        buttonText: function(methodName){
            if (methodName == this.$store.state.accountInfo.payment_method){
                return 'Click here to save changes'
            } else {
                return 'Select this method and save card data';
            }
        },
        sendToken: function(methodIndex, cardInfo){
            var self = this;
            var method = self.paymentMethods[methodIndex];
            httpService.post('/api/billing/paymentMethod', cardInfo).then(function(response){
                if (response && response.data.result){
                    method.success = 'You successfully entered payment data.';

                    // Updated user account info
                    self.$store.commit('updatePaymentInfo', response.data.info);
                } else {
                    method.error = 'Something went wrong. Please try again.';
                }
            }).catch(function(err){
                if (err){
                    method.error = 'Some error occured. Please try again.';
                }
            });
        },
        selectMethodAndSave: function(methodIndex){
            var self = this;
            var method = self.paymentMethods[methodIndex];
            if (!method){
                self.paymentMethods[0].error = 'For some reason a payment method not found... please try again.';
                return;
            }
            method.error = '';
            method.success = '';
            method.data.stripeApp.createToken(method.data.card).then(function(result) {
                if (result.error) {
                    method.error = result.error.message;
                } else {
                    var text_info = 'You current card is ****' + result.token.card.last4 + ', exp. on: ' + 
                        result.token.card.exp_month + '/' + result.token.card.exp_year;
                    var card_data = {
                        token: result.token.id,
                        name: method.name,
                        vendor: method.vendor_name,
                        text: text_info
                    };
                    self.sendToken(methodIndex, card_data);

                    // Update store user object 
                    self.$store.commit('updatePaymentText', text_info);
                    self.$store.commit('updatePaymentMethod', method.name);
                }
            });
        }
    }
}
</script>

<style>
    .StripeElement {
        background-color: white;
        height: 40px;
        padding: 10px 12px;
        border-radius: 4px;
        border: 1px solid #d0d1d2;
        box-shadow: 0 1px 3px 0 #e6ebf1;
        -webkit-transition: box-shadow 150ms ease;
        transition: box-shadow 150ms ease;
    }

    .StripeElement--focus {
        box-shadow: 0 1px 3px 0 #cfd7df;
    }

    .StripeElement--invalid {
        border-color: #fa755a;
    }

    .StripeElement--webkit-autofill {
        background-color: #fefde5 !important;
    }
    .select-method-block {
        position: relative;
        min-height: 60px;
    }
    .select-method-block button{
        position: absolute;
        margin-bottom: 0px;
        bottom: 0px;
    }
</style>