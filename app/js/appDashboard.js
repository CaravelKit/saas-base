import Vue from 'vue';
import VueRouter from 'vue-router';
import Vuex from 'vuex';
import $ from 'jquery';
import 'jquery.easing';
import 'popper.js';
import 'bootstrap';
var moment = require('moment');
import LeftMenu from './leftMenu.js';
import UserProfile from './views/dashboard/userProfile.vue';
import SamplePage from './views/dashboard/samplePage.vue';
import PageNotFound from './views/dashboard/pageNotFound.vue';
import Breadcrumbs from './views/dashboard/breadcrumbs.vue';
import Billing from './views/billing/billing.vue';
import Plan from './views/billing/plan.vue';
import BillingHistory from './views/billing/billingHistory.vue';
import Summary from './views/billing/summary.vue';
import PaymentMethod from './views/billing/paymentMethod.vue';

import UserRoutes from './userRoutes.js'

Vue.use(VueRouter);
Vue.use(Vuex);
const store = new Vuex.Store({
    state: {
        accountInfo: {},
        accountText: '',
        sideBarOpened: true
    },
    mutations: {
        /** Account/payment information **/
        updatePaymentInfo: function(state, newPaymentInfo) {
            state.accountInfo.payment_method_info = newPaymentInfo;
        },
        updatePaymentText: function(state, newPaymentText) {
            state.accountInfo.payment_method_text = newPaymentText;
        },
        updateAccountStatus: function(state, newStatus){
            state.accountInfo.account_status = newStatus;
        },
        updateAccountStatusText: function(state, newStatusText){
            state.accountInfo.account_status_text = newStatusText;
        },
        updateValidStatus: function(state, newStatus){
            state.accountInfo.valid_status = newStatus;
        },
        updatePaymentMethod: function(state, newMethod){
            state.accountInfo.payment_method = newMethod;
        },
        updatePlanId: function(state, newPlanId){
            state.accountInfo.plan_id = newPlanId;
        },
        updatePlanName: function(state, newPlanName){
            state.accountInfo.plan_name = newPlanName;
        },
        updateAccountInfo: function(state, newAccountInfo) {
            state.accountInfo = newAccountInfo;
        },
        /** Interface **/
        toggleSideBar: function(state){
            state.sideBarOpened = !state.sideBarOpened;
        }
    }
});

var routes = [
    { 
        path: '/user/profile', 
        component: UserProfile,
        name: 'userProfile',
        meta: {
            breadcrumb: [
                {   name: 'User'    },
                {   name: 'Profile' } // add 'link' field with name or the route
            ]
        } 
    },
    { 
        path: '/sample', component: SamplePage,
        meta: {
            breadcrumb: [
                {   name: 'Pages'    },
                {   name: 'Sample sub menu' } // add 'link' field with name or the route
            ]
        }  
    },
    {
        path: '/billing',
        component: Billing,
        name: 'billing',
        meta: {
            breadcrumb: [
                {   name: 'Billing'    }
            ]
        },
        children: [
            {path: '', component: Summary, meta: {
                breadcrumb: [{name: 'Billing'}]
            }},
            {   path: 'plan', 
                component: Plan, 
                meta: {
                    breadcrumb: [{name: 'Billing', link: '/billing'}, {name: 'Plan'}]
                }
            },
            {path: 'paymentMethod', component: PaymentMethod, meta: {
                breadcrumb: [{name: 'Billing', link: '/billing'}, {name: 'Payment methods'}]
            }},
            {path: 'billingHistory', component: BillingHistory, meta: {
                breadcrumb: [{name: 'Billing', link: '/billing'}, {name: 'Billing history'}]
            }}
        ]
    },
    { path: "*", component: PageNotFound }
];

routes = routes.concat(UserRoutes);

var router = new VueRouter({
    routes, 
    mode: 'history',
    linkExactActiveClass: 'active'
});

var timeFormatter = function(value){
    return (value ? moment(new Date("2015-06-17 14:24:36")).format("YYYY-MM-DD HH:mm:ss"): 'date/time is undefined');
};
Vue.filter('formatDt', timeFormatter);

new Vue({
    el: '#dashboardApp',
    components: { 
        'leftmenu': LeftMenu,
        SamplePage, 
        UserProfile, 
        Billing,
        'breadcrumbs': Breadcrumbs
    },
    router,
    store,
    data: {
    },
    methods: {
        toggleMenu: function(){
            this.$store.commit('toggleSideBar'); 
        }, 
        handleScroll: function(){
            100 < $(window.document).scrollTop() ? $(".scroll-to-top").fadeIn() : $(".scroll-to-top").fadeOut()
        },
        scrollToTop: function(event){
            var btn = $(event.currentTarget);
            $("html, body").stop().animate({
                scrollTop: $(btn.attr("href")).offset().top
            }, 1e3, "easeInOutExpo");
            event.preventDefault();
        },
        redirect: function(url){
            window.location.href = url;
        }
    },
    computed: {
        sideBarOpened() {
            return this.$store.state.sideBarOpened;
        }
    },
    created: function(){
        window.addEventListener('scroll', this.handleScroll);
    },
    destroyed: function(){
        window.removeEventListener('scroll', this.handleScroll);
    }
});