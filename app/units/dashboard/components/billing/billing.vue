<template>
    <div class="billing-options-block">
        <h3 class="title">Billing</h3>
        <div class="navigate-links">
            <router-link v-bind:to="'/dashboard/billing'" class="tab-link">Summary</router-link>
            <router-link v-bind:to="'/dashboard/billing/plan'" class="tab-link">Plan</router-link>
            <router-link v-bind:to="'/dashboard/billing/paymentMethod'" class="tab-link">Payment method</router-link>
            <router-link v-bind:to="'/dashboard/billing/billingHistory'" class="tab-link">Billing history</router-link>
        </div>
        <br>&nbsp;</br>
        <router-view></router-view>
    </div>
</template>

<script>
import { httpService } from '@app/units/common/httpService.js'; 
export default {
    name: 'Billing',
    data: function(){
        return {
            error: ''
        }
    },
    mounted: function(){
        var self = this;
        httpService.get('/api/billing/account').then(function(response){
            if (response && response.data.result){
                self.$store.commit('updateAccountInfo', response.data.info); 
            } else {
                self.error = 'Something went wrong. Please try again.';
            }
        }).catch(function(err){
            if (err){
                self.error = 'Some error occured. Please try again.';
            }
        });
    }
}
</script>

<style>
    @import '@app/units/dashboard/styles/billing/billingMenu.scss';
</style>