import Vue from 'vue';
import { httpService } from './../../common/httpService.js';

var app = new Vue({
    el: '#app_auth',
    data: {
        errors: [],
        data: {
            username: null,
            email: null,
            password: null, 
            password2: null,
            remember_me: true
        },
        valid: {
            username: false,
            email: false, 
            password: false,
            password2: false
        },
        resend_success: false
    },
    methods:{
        handleResponse: function(self, response){
            self.errors = [];
            if (response && response.data){
                for (var key in response.data.errors){
                    self.errors = self.errors.concat(response.data.errors[key]);
                }
                if (response.data.redirect){
                    window.location.href = response.data.redirect;
                }
            }
        },
        checkRegisterForm: function (e) {
            e.preventDefault();
            var self = this;
            if (this.data.username && 
                this.data.password && 
                this.data.email && 
                this.validEmail(this.data.email) && 
                this.data.password == this.data.password2) {
                    this.valid.username = true;
                    this.valid.email = true;
                    this.valid.password = true;
                    httpService.post('/register', this.data).then(function(response){
                        self.handleResponse(self, response);
                    }).catch(function(err){
                        if (err.message){
                            self.errors = [err.message];
                        }
                    });
            } else {
                this.errors = [];
    
                if (!this.data.username) {
                    this.errors.push('Please enter user name.');
                } else {
                    this.valid.username = true;
                }
                if (!this.data.email) {
                    this.errors.push('Please enter your email.');
                } else {
                    if (!this.validEmail(this.data.email)){
                        this.errors.push('Please enter a valid email.');
                    } else {
                        this.valid.email = true;
                    }
                }
                if (!this.data.password) {
                    this.errors.push('Please enter your password.');
                } else {
                    this.valid.password = true;
                }
                if (!this.data.password2) {
                    this.errors.push('Please confirm your password.');
                } else {
                    this.valid.password2 = true;
                }
                if (this.data.password != this.data.password2){
                    this.errors.push('Passwords should match.');
                } else {
                    this.valid.password2 = true;
                }
            } 
        },
        checkLoginForm: function (e) {
            e.preventDefault();
            var self = this;
            if (this.data.password && this.data.email && this.validEmail(this.data.email)) {
                this.valid.email = true;
                this.valid.password = true;
                httpService.post('/login', this.data).then(function(response){
                    self.handleResponse(self, response);
                }).catch(function(err){
                    if (err.message){
                        self.errors = [err.message];
                    }
                });
            } else {
                this.errors = [];
    
                if (!this.data.email) {
                    this.errors.push('Please enter your email.');
                } else {
                    if (!this.validEmail(this.data.email)){
                        this.errors.push('Please enter a valid email.');
                    } else {
                        this.valid.email = true;
                    }
                }
                if (!this.data.password) {
                    this.errors.push('Please enter your password.');
                } else {
                    this.valid.email = true;
                }
            } 
        },
        validEmail: function (email) {
            var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            return re.test(email);
        }
    }
});