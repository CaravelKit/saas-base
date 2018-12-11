<template>
    <div>
        <h5>Billing history</h5>
        <div class="row" v-show="loadingInProgress">
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
        <table class="table table-striped table-custom">
            <thead>
                <tr>
                    <th scope="col">Date</th>
                    <th scope="col">Event</th>
                    <th scope="col">Comment</th>
                </tr>
            </thead>
              <tbody>
                    <tr v-for="item in historyItems">
                        <td>{{item.date | format-dt}}</td>
                        <td>{{item.event}}</td>
                        <td>{{item.comment}}</td>
                    </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import { httpService } from '@app/js/common/httpService.js'; 

export default {
    name: 'BillingHistory',
    data() {
        return {
            columnDefs: null,
            historyItems: null, 
            error: '',
            success: '',
            loadingInProgress: false
        }
    },
    beforeMount() {
        var self = this;
        self.loadingInProgress = true;
        httpService.get('/api/billing/history').then(function(response){
            if (response && response.data.result){
               self.historyItems = response.data.info;
            } else {
                self.error = 'Something went wrong. Please try again.';
            }
        }).catch(function(err){
            if (err){
                self.error = 'Some error occured. Please try again.';
            }
        }).then(function(){
            self.loadingInProgress = false;
        });
    }
}
</script>

<style>
</style>