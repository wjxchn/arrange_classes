<template>
  <div class="show-result">
    <a-space direction="vertical" size="large" :style="{width: '600px'}" style="margin-bottom: 60px;">
      <a-radio-group v-model="layout" type="button">
        <a-radio value="byclassrooms">根据教室查看课表</a-radio>
        <a-radio value="byteachers">根据教师查看课表</a-radio>
        <a-radio value="bystudents">根据学生查看课表</a-radio>
      </a-radio-group>
    </a-space>
    <a-space v-show="layout=='byclassrooms'"  style="margin-bottom: 60px;">
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
    <a-space v-show="layout=='byteachers'"  style="margin-bottom: 60px;">
      教师名称
      <a-select
        v-model="teachervalue"
        :options="teacheroptions"
        :field-names="teacherfieldnames"
        :style="{width:'320px'}"
        placeholder="Please select ..."
        @dropdown-scroll="handleScroll"
        @dropdown-reach-bottom="handleReachBottom"
      >
      </a-select>
    </a-space>
    <a-space v-show="layout=='bystudents'"  style="margin-bottom: 60px;">
      学生名称
      <a-select
        v-model="studentvalue"
        :options="studentoptions"
        :field-names="studentfieldnames"
        :style="{width:'320px'}"
        placeholder="Please select ..."
        @dropdown-scroll="handleScroll"
        @dropdown-reach-bottom="handleReachBottom"
      >
      </a-select>
    </a-space>
    <a-table :columns="columns" :data="data" :pagination="ispagination" column-resizable/>
  </div>
</template>

<script>
import { reactive, ref, getCurrentInstance } from 'vue';

export default {
  setup() {
    const {proxy} = getCurrentInstance()
    const layout = ref('byclassrooms')
    const ispagination = false
    const handleScroll = (ev) => {
      console.log('scroll', ev)
    }
    const handleReachBottom = (ev) => {
      console.log('reach the bottom', ev)
    }
    const classroomvalue = ref('');
    const classroomfieldnames = {value: 'id', label: 'text'}
    const classroomoptions = reactive([]);
    const teachervalue = ref('');
    const teacherfieldnames = {value: 'id', label: 'text'}
    const teacheroptions = reactive([]);
    const studentvalue = ref('');
    const studentfieldnames = {value: 'id', label: 'text'}
    const studentoptions = reactive([]);
    const columns = [
      {
        title: '周一',
        dataIndex: 'monday',
      },
      {
        title: '周二',
        dataIndex: 'tuesday',
      },
      {
        title: '周三',
        dataIndex: 'wednesday',
      },
      {
        title: '周四',
        dataIndex: 'thursday',
      },
      {
        title: '周五',
        dataIndex: 'friday',
      },
      {
        title: '周六',
        dataIndex: 'saturday',
      },
      {
        title: '周日',
        dataIndex: 'sunday',
      },
    ];
    const data = reactive([]);
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
    return {
      columns,
      data,
      layout,
      ispagination,
      handleScroll,
      handleReachBottom,
      classroomvalue,
      classroomfieldnames,
      classroomoptions,
      teachervalue,
      teacherfieldnames,
      teacheroptions,
      studentvalue,
      studentfieldnames,
      studentoptions
    }
  },
}
</script>
<style scoped>
.show-result{
  padding-left:100px;
  padding-right: 100px;
  padding-top: 100px;
  padding-bottom: 100px;
}
</style>
