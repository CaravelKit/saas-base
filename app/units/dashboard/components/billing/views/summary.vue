<template>
    <div>
        <div class="row">
            <div class="col-12">
                <h5>Summary</h5>  
            </div>
        </div>
        <div class="row">
            <div class="col-12">
                <h6>Payment/trial info:</h6> 
                {{accountInfo.payment_method_text}}
                <br>
                {{accountInfo.account_status_text}}
                <br>
                <strong>Your current plan: </strong>{{accountInfo.plan_name || 'Plan is not yet selected.'}}
            </div>
        </div>
        <br>
        <div class="row" v-show="accountInfo.account_status=='trial' || !accountInfo.account_status || accountInfo.account_status=='cancelled'">
            <div class="col-12">
                <h6>Buy subscription</h6>
                To buy a subscription select a plan on <a href="/dashboard/billing/plan" class="inner-link">plans tab</a>.
            </div>
        </div>
        <div class="row" v-show="accountInfo.account_status=='paid'">
            <div class="col-12">
                <h6>To pause subscription:</h6>
            </div>
            <div class="col-12">
                <ul>
                    <li><a href="/dashboard/billing/plan" class="inner-link">Pause</a></li>
                </ul>
            </div>
        </div>
        <div class="row" v-show="accountInfo.account_status=='paid' || accountInfo.account_status=='paused'">
            <div class="col-12">
                <h6>To cancel subscription:</h6>
            </div>
            <div class="col-12">
                <ul>
                    <li><a href="/dashboard/billing/plan" class="inner-link">Cancel</a></li>
                </ul>
            </div>
        </div>
        <div class="row" v-show="accountInfo.account_status=='paused'">
            <div class="col-12">
                <h6>To resume subscription:</h6>
            </div>
            <div class="col-12">
                <ul>
                    <li><a href="/dashboard/billing/plan" class="inner-link">Resume</a></li>
                </ul>
            </div>
        </div>
        
    </div>
</template>

<script>
export default {
    name: 'Summary',
    computed: {
        paymentText() {
            return this.$store.state.accountInfo.payment_method_text;
        },
        accountText(){
            return this.$store.state.accountInfo.account_status_text;
        },
        accountInfo(){
            return this.$store.state.accountInfo;
        }
    }
}
</script>

<style>
</style>