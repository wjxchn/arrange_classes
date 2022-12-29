<template>
  <div class="show-result">
    <a-space direction="vertical" size="large" :style="{width: '600px'}" style="margin-bottom: 60px;">
      <a-radio-group v-model="layout" type="button">
        <a-radio value="byclassrooms">根据教室查看课表</a-radio>
        <a-radio value="byteachers">根据教师查看课表</a-radio>
        <a-radio value="bystudents">根据学生查看课表</a-radio>
      </a-radio-group>
    </a-space>
    <a-space v-show="layout=='byclassrooms'"  style="margin-bottom: 60px; margin-left:20px;">
      教室名称
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
    <a-space v-show="layout=='byteachers'"  style="margin-bottom: 60px; margin-left:20px;">
      教师名称
      <a-select
        allow-search
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
    <a-space v-show="layout=='bystudents'"  style="margin-bottom: 60px; margin-left:20px;">
      学生名称
      <a-select
        allow-search
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
    <a-space style="margin-bottom: 60px; margin-left:20px;">
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
    <a-space style="margin-bottom: 60px; margin-left:20px;">
      <a-button type="primary" @click="getdata">确定</a-button>
    </a-space>
    <a-table :columns="columns" :data="data" :pagination="ispagination" column-resizable/>
  </div>
</template>

<script>
import { reactive, ref, getCurrentInstance } from 'vue';
import qs from 'qs'
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
    const resultvalue = ref('');
    const resultfieldnames = {value: 'id', label: 'text'}
    const resultoptions = reactive([]);
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
    const getTeacherData = function(){
      proxy.$http.get("getteacher/").then((res) => {
        console.log(res);
        res.data.teachers.forEach(element => {
          teacheroptions.push({
            id: element.teacher_id,
            text: element.name,
          })
        });
      }) .catch((res) => {
        console.log(res);
      });
    }
    getTeacherData()
    const getStudentData = function(){
      proxy.$http.get("getstudent/").then((res) => {
        console.log(res);
        res.data.students.forEach(element => {
          studentoptions.push({
            id: element.student_id,
            text: element.name,
          })
        });
      }) .catch((res) => {
        console.log(res);
      });
    }
    getStudentData()
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
    const getdata = function(){
      if(layout.value == 'byclassrooms'){
        console.log(classroomvalue.value)
        console.log(resultvalue.value)
        proxy.$http.post("getcoursetablebyclassroom/", qs.stringify({"result_file_name": resultvalue.value, "classroom_id": classroomvalue.value}))
          .then((res) => {
          console.log(res);
          while(data.length!=0){
            data.pop()
          }
          for (var i=0;i<14;i++) {
            data.push({})
          }
          for (var i=1;i<=14;i++) {
            console.log(res.data.res[i])
            var res_item
            for (res_item in res.data.res[i]){
              console.log(res.data.res[i][res_item])
              data[i-1][res_item] = res.data.res[i][res_item]
            }
          }
        }) .catch((res) => {
          console.log(res);
        });
      }
      else if(layout.value == 'byteachers'){
        console.log(teachervalue.value)
        console.log(resultvalue.value)
        proxy.$http.post("getcoursetablebyteacher/", qs.stringify({"result_file_name": resultvalue.value, "teacher_id": teachervalue.value}))
          .then((res) => {
          console.log(res);
          while(data.length!=0){
            data.pop()
          }
          for (var i=0;i<14;i++) {
            data.push({})
          }
          for (var i=1;i<=14;i++) {
            console.log(res.data.res[i])
            var res_item
            for (res_item in res.data.res[i]){
              console.log(res.data.res[i][res_item])
              data[i-1][res_item] = res.data.res[i][res_item]
            }
          }
        }) .catch((res) => {
          console.log(res);
        });
      }
      else if(layout.value == 'bystudents'){
        console.log(studentvalue.value)
        console.log(resultvalue.value)
        proxy.$http.post("getcoursetablebystudent/", qs.stringify({"result_file_name": resultvalue.value, "student_id": studentvalue.value}))
          .then((res) => {
          console.log(res);
          while(data.length!=0){
            data.pop()
          }
          for (var i=0;i<14;i++) {
            data.push({})
          }
          for (var i=1;i<=14;i++) {
            console.log(res.data.res[i])
            var res_item
            for (res_item in res.data.res[i]){
              console.log(res.data.res[i][res_item])
              data[i-1][res_item] = res.data.res[i][res_item]
            }
          }
        }) .catch((res) => {
          console.log(res);
        });
      }
      
    }
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
      studentoptions,
      resultvalue,
      resultfieldnames,
      resultoptions,
      getdata
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
