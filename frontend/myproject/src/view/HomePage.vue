<template>
  <div class="home-page">
    <a-space direction="vertical" size="large" :style="{width: '600px'}"  style="margin-bottom: 60px;">
      <a-radio-group v-model="layout" type="button">
        <a-radio value="autoarrange">自动排课</a-radio>
        <a-radio value="manualchange">手动调整排课</a-radio>
      </a-radio-group>
    </a-space>
    <a-space v-show="layout=='autoarrange'" style="margin-bottom: 60px; margin-left:20px;">
      <a-button type="primary" @click="arrangefunc">排课</a-button>
    </a-space>
    <a-space v-show="layout=='manualchange'" style="margin-bottom: 60px; margin-left:20px;">
      课程名称
      <a-select
        allow-search
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
      新教室名称
      <a-select
        allow-search
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
        allow-search
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
    <a-space v-show="layout=='manualchange'" style="margin-bottom: 60px; margin-left:20px;">
      选择排课结果
      <a-select
        allow-search
        v-model="resultvalue"
        :options="resultoptions"
        :field-names="resultfieldnames"
        :style="{width:'320px'}"
        placeholder="Please select ..."
        @dropdown-scroll="handleScroll"
        @dropdown-reach-bottom="handleReachBottom"
      >
      </a-select>
    </a-space>
    <a-space v-show="layout=='manualchange'" style="margin-bottom: 60px; margin-left:20px;">
      重新排课的开始周次
      <a-input-number v-model="weekstartvalue" :style="{width:'320px'}" placeholder="Please Enter" class="input-demo" :min="0" :max="100"/>
    </a-space>
    <a-space v-show="layout=='manualchange'" style="margin-bottom: 60px; margin-left:20px;">
      重新排课的结束周次
      <a-input-number v-model="weekendvalue" :style="{width:'320px'}" placeholder="Please Enter" class="input-demo" :min="0" :max="100"/>
    </a-space>
    <a-space v-show="layout=='manualchange'" style="margin-bottom: 60px; margin-left:20px;">
      <a-button type="primary" @click="manualarrangefunc">确定</a-button>
    </a-space>
  </div>
</template>

<script>
import { reactive, ref, getCurrentInstance } from 'vue';
import qs from 'qs'
export default {
  setup() {
    const weekstartvalue = ref(0)
    const weekendvalue = ref(0)
    const {proxy} = getCurrentInstance()
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
    const modeoptions = reactive([
      {
        id: 'update',
        text: '更新'
      },
      {
        id: 'add',
        text: '新增'
      },
      {
        id: 'del',
        text: '删除'
      }
    ]);
    const resultvalue = ref('');
    const resultfieldnames = {value: 'id', label: 'text'}
    const resultoptions = reactive([])
    const getCourseData = function(){
      proxy.$http.get("getclass/").then((res) => {
        console.log(res);
        res.data.classrooms.forEach(element => {
          courseoptions.push({
            id: element.id,
            text: element.name,
          })
        });
      }) .catch((res) => {
        console.log(res);
      });
    }
    getCourseData()
    const getClassroomData = function(){
      proxy.$http.get("getclassroom/").then((res) => {
        console.log(res);
        res.data.classrooms.forEach(element => {
          classroomoptions.push({
            id: element.id,
            text: element.name,
          })
        });
      }) .catch((res) => {
        console.log(res);
      });
    }
    getClassroomData()
    const getResultData = function(){
      proxy.$http.get("getresultlist/").then((res) => {
        console.log(res);
        res.data.result_list.forEach(element => {
          resultoptions.push({
            id: element,
            text: element,
          })
        });
      }) .catch((res) => {
        console.log(res);
      });
    }
    getResultData()
    const arrangefunc = function(){
      alert('点击确定后排课，排课在后台进行，几分钟后刷新会有结果')
      proxy.$http.post("arrangeclass/").then((res) => {
      }) .catch((res) => {
      });
    }
    const manualarrangefunc = function(){
      proxy.$http.post("manualchangeclasstable/", qs.stringify({
        result_file_name: resultvalue.value,
        course_id: coursevalue.value,
        classroom_id: classroomvalue.value,
        st_week: weekstartvalue.value,
        ed_week: weekendvalue.value,
        mode: modevalue.value
      })).then((res) => {
        console.log(res);
        if(res.data.code==200){
          alert('手动重排成功')
        }
        else{
          alert('手动排课失败')
        }
      }) .catch((res) => {
        console.log(res);
        alert('手动排课失败')
      });
    }
    return {
      weekstartvalue,
      weekendvalue,
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
      modeoptions,
      resultvalue,
      resultfieldnames,
      resultoptions,
      arrangefunc,
      manualarrangefunc
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