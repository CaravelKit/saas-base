import Vue from 'vue';
import VueRouter from 'vue-router';
import 'bootstrap';

<template>
    <div v-show="breadcrumbList">
        <ol class="breadcrumb">
            <li class="breadcrumb-item"
                v-for="(breadcrumb, index) in breadcrumbList"
                :key="index"
                @click="routeTo(index)"
                :class="{'active': breadcrumb.link}">
                <span v-show="!breadcrumb.link">{{ breadcrumb.name }}</span>
                <a v-bind:href="breadcrumb.link" v-show="breadcrumb.link">{{ breadcrumb.name }}</a>
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
    routeTo (routeIndex) {
      if (this.breadcrumbList[routeIndex].link) this.$router.push(this.breadcrumbList[routeIndex].link)
    },
    updateList () { this.breadcrumbList = this.$route.meta.breadcrumb }
  }
}
</script>

<style>
</style>