import Vue from 'vue';
import VueRouter from 'vue-router';
import $ from 'jquery';
import 'jquery.easing';
import 'popper.js';
import 'bootstrap';
import UserProfile from './views/userProfile.vue';
import SamplePage from './views/samplePage.vue';
import PageNotFound from './views/pageNotFound.vue';

Vue.use(VueRouter);

var routes = [
    { path: '/dashboard', component: SamplePage },
    { path: '/dashboard/user/profile', component: UserProfile },
    { path: '/dashboard/sample', component: SamplePage },
    { path: "*", component: PageNotFound }
];

var router = new VueRouter({
    routes, 
    mode: 'history'
});

new Vue({
    el: '#dashboardApp',
    components: { SamplePage, UserProfile },
    router,
    data: {
        sideBarOpened: true
    },
    methods: {
        toggleMenu: function(){
            this.sideBarOpened = !this.sideBarOpened;
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
        }
    },
    created: function(){
        window.addEventListener('scroll', this.handleScroll);
    },
    destroyed: function(){
        window.removeEventListener('scroll', this.handleScroll);
    }
});