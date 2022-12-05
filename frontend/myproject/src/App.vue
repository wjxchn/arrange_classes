<template>
  <div>
    <top-header></top-header>
    <router-view></router-view>
  </div>
</template>

<script>
import TopHeader from './components/TopHeader.vue'

export default {
  name: 'App',
  components: {
    TopHeader
  }
}
</script>

<style>

</style>
