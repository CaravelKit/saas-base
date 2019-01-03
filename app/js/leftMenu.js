import { commonService } from '@app/js/common/commonService.js'; 
export default {
    name: 'LeftMenu',
    template: require('./../templates/leftMenu.html'),
    data() {
        return {
        }
    },
    methods: {
        openUrl: function(routeName, params){
            console.log(routeName);
            commonService.redirectToRoute(this, routeName, params);
        }
    },
    computed: {
        sideBarOpened() {
            return this.$store.state.sideBarOpened;
        }
    }
}
