import Vue from 'vue';
import VueRouter from 'vue-router';
import 'bootstrap';

<template>
    <div v-show="breadcrumbList">
        <ol class="breadcrumb">
            <li class="breadcrumb-item"
                v-for="(breadcrumb, index) in breadcrumbList"
                :key="index"
                :class="{'active': breadcrumb.link}">
                <span v-show="!shouldBeLink(breadcrumb)">{{ breadcrumb.name }}</span>
                <!--a v-bind:href="breadcrumb.link" v-show="breadcrumb.link">{{ breadcrumb.name }}</a -->
                <router-link v-show="shouldBeLink(breadcrumb)" :to="{ name: breadcrumb.route, params: breadcrumb.params || {}}">
                    {{ breadcrumb.name }}==
                </router-link>
                
            </li>
        </ol>
    </div>
</template>

<script>
export default {
  name: 'Breadcrumb',
  data () {
    return {
      breadcrumbList: []
    }
  },
  mounted () { this.updateList() },
  watch: { '$route' () { this.updateList() } },
  methods: {
    shouldBeLink: function(breadcrumb){
        if (breadcrumb.route){
            return breadcrumb.route != this.$route.name;
        } else if (breadcrumb.link) {
            return breadcrumb.link != this.$route.path;
        } 
        return false;
    },
    routeTo: function(index){
        if (this.breadcrumbList[routeIndex].link) {
            this.$router.push(this.breadcrumbList[routeIndex].link);
            return;
        }
        if (this.breadcrumbList[routeIndex].route) {
            var routeObject = {
                name: this.breadcrumbList[routeIndex].route
            };
            if (this.breadcrumbList[routeIndex].params){
                routeObject.params = this.breadcrumbList[routeIndex].params;
            }
            this.$router.push(routeObject);
        }
    },
    updateList () { 
        this.breadcrumbList = this.$route.meta.breadcrumb;
    }
  }
}
</script>

<style>
</style>