<template>
    <div id="userProfile" class="container-fluid">
        <div class="col-lg-6">
            <h3>User profile</h3>
            <div class="form-group">
                <label>User name</label>
                <input type="text" class="form-control" v-model="userdata.username"/>
            </div>
            <div class="form-group form-check">
                <input type="checkbox" class="form-check-input" id="subscribeBox" v-model="userdata.subscribed">
                <label class="form-check-label" for="subscribeBox">Send me updates and news</label>
            </div>
            <div>
                <button class="btn btn-primary" @click="saveUserProfile">Save</button>
            </div>
            <div class="alert alert-danger" role="alert" v-show="errorMessage">
                {{errorMessage}}
            </div>
            <div class="alert alert-success" role="alert" v-show="successMessage">
                {{successMessage}}
            </div>
        </div>
    </div>
</template>

<script>
    //const axios = require('axios');
    import { httpService } from '@app/components/common/httpService.js'; 
    export default {
        name: 'UserProfile',
        data: function(){
            return {
                userdata: {
                    username: '',
                    subscribed: false
                }, 
                errorMessage: '', 
                successMessage: ''
            };
        },
        created: function(){
            var self = this;
            
            httpService.get('/api/userdata').then(function(response){
                if (response && response.data.result && response.data.userdata){
                    self.userdata = response.data.userdata;
                } else {
                    self.errorMessage = 'Something went wrong. Please try again.';
                }
            }).catch(function(err){
                if (err){
                    if (err.request.status == 500){
                        // Show error message // to-do: the error message should be got from the server, not generated here.
                        self.errorMessage = 'Some error occured. Please try again.';
                    }
                }
            });
        },
        methods: {
            saveUserProfile: function(){
                var self = this;
                httpService.post('/api/userdata', self.userdata).then(function(response){
                    if (response && response.data.result){
                        self.successMessage = 'Your profile information has been updated! You now can reload this page to see a result.';
                    } else {
                        self.errorMessage = 'Something went wrong. Please try again.';
                    }
                }).catch(function(err){
                    if (err){
                        if (err.request.status == 500){
                            self.errorMessage = 'Some error occured. Please try again.';
                        }
                    }
                });
            }
        }
    }
</script>

<style>

</style>