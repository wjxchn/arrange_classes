<template>
  <div class="home-page">
    <a-space direction="vertical" size="large" :style="{width: '600px'}"  style="margin-bottom: 60px;">
      <a-radio-group v-model="layout" type="button">
        <a-radio value="autoarrange">自动排课</a-radio>
        <a-radio value="autochange">自动调整排课</a-radio>
        <a-radio value="manualchange">手动调整排课</a-radio>
      </a-radio-group>
    </a-space>
    <a-space v-show="layout=='autoarrange'" style="margin-bottom: 60px; margin-left:20px;">黑</a-space>
    <a-space v-show="layout=='autochange'" style="margin-bottom: 60px; margin-left:20px;">白</a-space>
    <a-space v-show="layout=='manualchange'" style="margin-bottom: 60px; margin-left:20px;">
      课程名称
      <a-select
        v-model="coursevalue"
        :options="courseoptions"
        :field-names="coursefieldnames"
        :style="{width:'320px'}"
        placeholder="Please select ..."
        @dropdown-scroll="handleScroll"
        @dropdown-reach-bottom="handleReachBottom"
      >
      </a-select>
    </a-space>
    <a-space v-show="layout=='manualchange'" style="margin-bottom: 60px; margin-left:20px;">
      教室名称
      <a-select
        v-model="classroomvalue"
        :options="classroomoptions"
        :field-names="classroomfieldnames"
        :style="{width:'320px'}"
        placeholder="Please select ..."
        @dropdown-scroll="handleScroll"
        @dropdown-reach-bottom="handleReachBottom"
      >
      </a-select>
    </a-space>
    <a-space v-show="layout=='manualchange'" style="margin-bottom: 60px; margin-left:20px;">
      选择模式
      <a-select
        v-model="modevalue"
        :options="modeoptions"
        :field-names="modefieldnames"
        :style="{width:'320px'}"
        placeholder="Please select ..."
        @dropdown-scroll="handleScroll"
        @dropdown-reach-bottom="handleReachBottom"
      >
      </a-select>
    </a-space>
  </div>
</template>

<script>
import { reactive, ref } from 'vue';

export default {
  setup() {
    const layout = ref('autoarrange')
    const handleScroll = (ev) => {
      console.log('scroll', ev)
    }
    const handleReachBottom = (ev) => {
      console.log('reach the bottom', ev)
    }
    const coursevalue = ref('');
    const coursefieldnames = {value: 'id', label: 'text'}
    const courseoptions = reactive([]);
    const classroomvalue = ref('');
    const classroomfieldnames = {value: 'id', label: 'text'}
    const classroomoptions = reactive([]);
    const modevalue = ref('');
    const modefieldnames = {value: 'id', label: 'text'}
    const modeoptions = reactive([]);
    return {
      layout,
      handleScroll,
      handleReachBottom,
      coursevalue,
      coursefieldnames,
      courseoptions,
      classroomvalue,
      classroomfieldnames,
      classroomoptions,
      modevalue,
      modefieldnames,
      modeoptions
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