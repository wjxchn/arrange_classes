<template>
  <div class="home-page">
    <a-space direction="vertical" size="large" :style="{width: '600px'}">
      <a-radio-group v-model="layout" type="button">
        <a-radio value="autoarrange">自动排课</a-radio>
        <a-radio value="autochange">自动调整排课</a-radio>
        <a-radio value="manualchange">手动调整排课</a-radio>
      </a-radio-group>
    </a-space>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const layout = ref('autoarrange')
    return {
      layout,
    }
  },
}
</script>
<style scoped>
.home-page{
  padding-left:100px;
  padding-right: 100px;
  padding-top: 100px;
  padding-bottom: 100px;
}
</style>