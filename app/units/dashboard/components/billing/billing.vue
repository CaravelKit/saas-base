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
    .billing-options-block a.tab-link {
        display: inline-block;
        padding: 5px 20px;
        border-radius: 10px;
        background-color: #7fabd8;
        color: #091e33;
    }
    .billing-options-block a.tab-link:hover {
        background-color: #62a5ea;
        color: #f5f6f7;
        text-decoration: none;
    }
    .billing-options-block .tab-link.active, .billing-options-block .tab-link.active:hover, 
    .billing-options-block .tab-link.active a:hover {
        font-weight: bold;
        cursor: default;
        color: #091e33;
        background-color: #7fabd8;
    }
    .billing-options-block .navigate-links {
        display: inline-block;
        float: right;
    }
    .billing-options-block .title {
        display: inline-block;
    }
    .billing-options-block a.inner-link {
        color: #145ba1;
        text-decoration: none;
    }
    .billing-options-block a.inner-link:hover {
        color: #1a7cdd;
        text-decoration: underline;
    }
    .billing-options-block a.inner-link-disabled, .billing-options-block a.inner-link-disabled:hover{
        cursor: default;
        text-decoration: none;
    }
    .billing-options-block .info-small-block {
        font-size: smaller;
        margin-top: 15px;
    }
</style>