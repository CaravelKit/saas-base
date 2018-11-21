export default {
    name: 'LeftMenu',
    template: require('./../templates/leftMenu.html'),
    data() {
        return {
        }
    },
    methods: {
        openUrl: function(routeName, params){
            var routeObject = {
                name: routeName
            };
            if (params){
                routeObject.params = params;
            }
            this.$router.push(routeObject);
        }
    },
    computed: {
        sideBarOpened() {
            return this.$store.state.sideBarOpened;
        }
    }
}
