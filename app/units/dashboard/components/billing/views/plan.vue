<template>
    <div class="billing-price">
        <h5>Select or change the current plan</h5>
        <div class="row" v-show="!plans.length">
            <div class="col-12 text-center">
                <i class="fas fa-cog fa-spin loader"></i>
            </div>
        </div>
        <div class="row">
            <div class="col-12">
                <div id="card-errors" role="alert" class="alert alert-danger" v-show="error">{{error}}</div>
                <div role="alert" class="alert alert-success" v-show="success">{{success}}</div>
            </div>
        </div>
        <div class="row plan-block" v-for="plan in plans" v-show="plans.length">
            <div class="col-8">
                <h4>{{plan.data.name}}</h4>
                <div class="price-info">
                    <span class="price">{{plan.data.price}} {{plan.data.currency}}</span>
                    <span v-show="plan.data.interval">/ {{plan.data.interval_count}} {{plan.data.interval}}</span>
                </div>
                <div v-show="plan.data.description">
                    <span class="plan-title">Description:</span> <span>{{plan.data.description}}</span>
                </div>
                
                <div v-show="plan.data.features.length > 0">
                    <span class="plan-title">Features:</span>
                    <ul class="features">
                        <li v-for="feature in plan.data.features">{{feature}}</li>
                    </ul>
                </div>
            </div>
            <div class="col-4 text-center">
                <!-- button class="btn btn-primary" @click="selectAndStartTrial(index)" v-show="isTrialAvailable()">Start a trial</button>
                <div v-show="isPlanInUse(plan.data.id)">
                    <i class="fas fa-check icon-green"></i><span>Trial started</span>
                </div -->
                <br>
                <div v-show="plan.data.id == $store.state.accountInfo.plan_id">
                    <div>
                        <i class="fas fa-check icon-green"></i><span>Selected plan{{selectedPlanAdditionalStatus}}</span>
                    </div>
                    <div v-show="$store.state.accountInfo.account_status == 'paid'">
                        <button class="btn btn-pause" @click="pausePlan(plan)">Pause</button>
                        <button class="btn btn-cancel" @click="cancelPlan(plan)">Cancel</button>
                    </div>
                    <div v-show="$store.state.accountInfo.account_status == 'paused'">
                        <button class="btn btn-resume" @click="selectSubscriptionToBuy(plan)">Resume</button>
                        <button class="btn btn-cancel" @click="cancelPlan(plan)">Cancel</button>
                    </div>
                </div>
                <div v-show="plan.data.id != $store.state.accountInfo.plan_id || 
                    ($store.state.accountInfo.account_status != 'paid' && $store.state.accountInfo.account_status != 'paused')">
                    <button class="btn btn-primary" @click="selectSubscriptionToBuy(plan)">Buy a subscription</button>
                </div>
            </div>
        </div>
        <div class="modal fade" id="paymentMethodModal" tabindex="-1" role="dialog" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">Payment method</h5>
                        <button class="close" type="button" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">×</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <payment-methods></payment-methods>
                    </div>
                    <div class="modal-footer container">
                        <div class="row">
                            <div class="modal-footer-info col-6">
                                <select v-model="selectedPlan" class="form-control">
                                    <option v-for="plan in plans" v-bind:value="plan">
                                        {{ plan.data.name }}
                                    </option>
                                </select>
                            </div>
                            <div class="modal-footer-buttons-block col-6 text-right">
                                <button class="btn btn-secondary" type="button" data-dismiss="modal" :disabled="buyInProgress">Cancel</button>
                                <button class="btn btn-primary" @click="buySubscription($event)" 
                                    :disabled="!$store.state.accountInfo.payment_method">
                                    Buy subscription
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="modal fade" id="cancelSuscriptionModal" tabindex="-1" role="dialog" aria-hidden="true">
            <div class="modal-dialog-small modal-dialog modal-dialog-centered" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">Cancel subscription?</h5>
                        <button class="close" type="button" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">×</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <h6>Are you sure to cancel subscription to plan "{{cancellingPlanName}}"?</h6>
                        <span>You will not be able to use the service after {{paymentExpiration}}.</span>
                    </div>
                    <div class="modal-footer container">
                        <div class="row">
                            <div class="modal-footer-buttons-block col-12 text-right">
                                <button class="btn btn-secondary" type="button" data-dismiss="modal" 
                                    @click="closeCancelSubscription()" :disabled="cancelInProgress">Close</button>
                                <button class="btn btn-primary" @click="cancelSubscription($event)" 
                                    :disabled="!$store.state.accountInfo.payment_method">
                                    Cancel subscription
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="modal fade" id="pauseSuscriptionModal" tabindex="-1" role="dialog" aria-hidden="true">
            <div class="modal-dialog-small modal-dialog modal-dialog-centered" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">Pause subscription?</h5>
                        <button class="close" type="button" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">×</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <h6>Are you sure to pause subscription to plan "{{pausingPlanName}}"?</h6>
                        <span>You will not be able to use the service after {{paymentExpiration}}.</span>
                    </div>
                    <div class="modal-footer container">
                        <div class="row">
                            <div class="modal-footer-buttons-block col-12 text-right">
                                <button class="btn btn-secondary" type="button" data-dismiss="modal" 
                                    @click="closePauseSubscription()" :disabled="pauseInProgress">Close</button>
                                <button class="btn btn-primary" @click="pauseSubscription($event)" 
                                    :disabled="!$store.state.accountInfo.payment_method">
                                    Pause subscription
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { commonService } from '@app/units/common/commonService.js'; 
import { httpService } from '@app/units/common/httpService.js'; 
import _ from 'lodash';
import $ from 'jquery';
import PaymentMethod from './paymentMethod.vue';
export default {
    name: 'Plan',
    components: {
        'payment-methods': PaymentMethod
    },
    data: function(){
        return {
            plans: [],
            error: '',
            success: '',
            selectedPlan: null,
            cancellingPlan: null,
            cancellingPlanName: '',
            pausingPlan: null,
            pausingPlanName: '',
            buttonWaiting: null,
            buyInProgress: false,
            cancelInProgress: false,
            pauseInProgress: false
        };
    },
    computed: {
        paymentExpiration() {
            return this.$store.state.accountInfo.payment_expiration;
        },
        selectedPlanAdditionalStatus(){
            if (this.$store.state.accountInfo.account_status && this.$store.state.accountInfo.account_status != 'paid'){
                return ' (' +  this.$store.state.accountInfo.account_status + ')';
            }
        }
    },
    created: function(){
        var self = this;
        self.error = '';
        self.success = '';
        httpService.get('/api/billing/plan/list').then(function(response){
            if (response && response.data.result && response.data.plans){
                self.plans = _.map(response.data.plans, function(plan){
                    var planObject = {};
                    planObject.data = plan;
                    planObject.error = '';
                    planObject.success = '';
                    return planObject;
                });
            } else {
                self.error = 'Something went wrong. Please try again.';
            }
        }).catch(function(err){
            if (err){
                if (err.request.status == 500){
                    // Show error message // to-do: the error message should be got from the server, not generated here.
                    self.error = 'Some error occured. Please try again.';
                }
            }
        });
    },
    methods: {
        selectAndStartTrial: function(planIndex){
            var self = this;
            var plan = self.plans[planIndex];
            if (!plan){
                return; // to-so: error message?
            }
            var data = {
                planId: plan.data.id
            };
            httpService.post('/api/billing/plan/trial', data).then(function(response){
                if (response && response.data.result){
                    self.$store.commit('updatePaymentText', response.data.text);
                    self.$store.commit('updateAccountStatus', response.data.status);
                    self.$store.commit('updateValidStatus', response.data.valid);
                    self.success = response.data.text;
                } else {
                    self.error = response.data.message || 'Something went wrong. Please try again.';
                }
            }).catch(function(err){
                if (err){
                    self.error = 'Some error occured. Please try again.';
                }
            });
        },
        isPlanInUse: function(planId){
            if (this.$store.state.accountInfo.plan_id == planId && this.$store.state.accountInfo.account_status == 'trial'){
                return true;
            }
            return false;
        },
        isTrialAvailable: function(){
            return this.$store.state.accountInfo.account_status == null;
        },
        selectSubscriptionToBuy: function(plan){
            this.selectedPlan = plan;
            $('#paymentMethodModal').modal();
        },
        buySubscription: function(event){
            commonService.startLoader($(event.target), 'Please, wait...');
            this.error = '';
            if (!(this.$store.state.accountInfo.payment_method && this.$store.state.accountInfo.payment_method_info)){
                this.error = 'To buy a subscription you have to enter you payment method information.'
            }
            if (!(this.selectedPlan && this.selectedPlan.data.id)){
                this.error += (this.error ? '\n' : '');
                this.error = this.error += 'To buy a subscription you have to select a plan.'
            }
            if (this.error){
                return;
            }
            var data = {
                plan_id: this.selectedPlan.data.id,
                plan_name: this.selectedPlan.data.name
            };
            var self = this;
            self.buyInProgress = true;
            httpService.post('/api/billing/subscription', data).then(function(response){
                if (response && response.data.result){
                    self.$store.commit('updateAccountStatus', response.data.account_status);
                    self.$store.commit('updateAccountStatusText', response.data.account_status_text);
                    self.$store.commit('updatePaymentText', response.data.payment_method_text);
                    self.$store.commit('updatePlanId', data.plan_id);
                    self.$store.commit('updatePlanName', data.plan_name);
                    self.success = response.data.account_status_text;
                } else {
                    self.error = response.data.message || 'Something went wrong. Please try again.';
                }
            }).catch(function(err){
                if (err && err.request){
                    if (err.request.status == 500){
                        self.error = 'Some error occured. Please try again.'
                    }
                } else {
                    self.error = (err && err.message) || 'Some error occured. Please try again.';
                }
            }).then(function(){
                self.buyInProgress = false;
                $('#paymentMethodModal').modal('hide');
                commonService.stopLoader($(event.target));
            });
        },
        cancelPlan: function(plan){
            this.cancellingPlan = plan;
            this.cancellingPlanName = plan.data.name;
            $('#cancelSuscriptionModal').modal();
        },
        closeCancelSubscription: function(){
            this.cancellingPlan = null;
            this.cancellingPlanName = '';
            if (this.buttonWaiting){
                commonService.stopLoader(this.buttonWaiting);
            }
            $('#cancelSuscriptionModal').modal('hide');
        },
        pausePlan: function(plan){
            this.pausingPlan = plan;
            this.pausingPlanName = plan.data.name;
            $('#pauseSuscriptionModal').modal();
        },
        closePauseSubscription: function(){
            this.pausingPlan = null;
            this.pausingPlanName = '';
            if (this.buttonWaiting){
                commonService.stopLoader(this.buttonWaiting);
            }
            $('#pauseSuscriptionModal').modal('hide');
        },
        cancelSubscription: function(event){
            var self = this;
            self.buttonWaiting = $(event.target);
            self.cancelInProgress = true;
            commonService.startLoader(self.buttonWaiting, 'Please, wait...')
            httpService.post('/api/billing/subscription/cancelpause').then(function(response){
                if (response && response.data.result){
                    self.$store.commit('updateAccountStatus', response.data.account_status);
                    self.$store.commit('updateAccountStatusText', response.data.account_status_text);
                    self.success = response.data.account_status_text;
                } else {
                    self.error = response.data.message || 'Something went wrong. Please try again.';
                }
            }).catch(function(err){
                if (err && err.request){
                    if (err.request.status == 500){
                        self.error = 'Some error occured. Please try again.'
                    }
                } else {
                    self.error = (err && err.message) || 'Some error occured. Please try again.';
                }
            }).then(function(){
                self.cancelInProgress = false;
                $('#cancelSuscriptionModal').modal('hide');
                commonService.stopLoader(self.buttonWaiting);
            });
        },
        pauseSubscription: function(event){
            var self = this;
            self.buttonWaiting = $(event.target);
            self.pauseInProgress = true;
            commonService.startLoader(self.buttonWaiting, 'Please, wait...');
            var data = {
                pause: true
            };
            httpService.post('/api/billing/subscription/cancelpause', data).then(function(response){
                if (response && response.data.result){
                    self.$store.commit('updateAccountStatus', response.data.account_status);
                    self.$store.commit('updateAccountStatusText', response.data.account_status_text);
                    self.success = response.data.account_status_text;
                } else {
                    self.error = response.data.message || 'Something went wrong. Please try again.';
                }
            }).catch(function(err){
                if (err && err.request){
                    if (err.request.status == 500){
                        self.error = 'Some error occured. Please try again.'
                    }
                } else {
                    self.error = (err && err.message) || 'Some error occured. Please try again.';
                }
            }).then(function(){
                self.pauseInProgress = false;
                $('#pauseSuscriptionModal').modal('hide');
                commonService.stopLoader(self.buttonWaiting);
            });
        }
    }
}
</script>

<style lang="scss">
    @import '@app/units/dashboard/styles/billing/billing.scss';
</style>