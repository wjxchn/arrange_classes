<template>
  <div class="govern-data">
    <a-space direction="vertical" size="large" :style="{width: '600px'}" style="margin-bottom: 60px;">
      <a-radio-group v-model="layout" type="button">
        <a-radio value="byclassrooms">管理教室信息</a-radio>
        <a-radio value="byclasses">管理课程信息</a-radio>
        <a-radio value="byusers">管理用户信息</a-radio>
      </a-radio-group>
    </a-space>
    <a-table v-show="layout=='byclassrooms'" :columns="classroom_columns" :data="classroom_data" :pagination="ispagination" column-resizable>
      <template #optional="{ record }">
        <a-button @click="classroom_handleClick(record)">编辑教室信息</a-button>
        <a-modal v-model:visible="classroom_visible_var" @ok="classroom_handleOk" @cancel="classroom_handleCancel">
          <template #title>
            Title
          </template>
          <div>显示的是编辑教室信息</div>
        </a-modal>
      </template>
    </a-table>
    <a-table v-show="layout=='byclasses'" :columns="class_columns" :data="class_data" :pagination="ispagination" column-resizable>
      <template #optional="{ record }">
        <a-button @click="class_handleClick(record)">编辑课程信息</a-button>
        <a-modal v-model:visible="class_visible_var" @ok="class_handleOk" @cancel="class_handleCancel">
          <template #title>
            Title
          </template>
          <div>显示的是编辑课程信息</div>
        </a-modal>
      </template>
    </a-table>
    <a-table v-show="layout=='byusers'" :columns="user_columns" :data="user_data" :pagination="ispagination" column-resizable>
      <template #optional="{ record }">
        <a-button @click="user_handleClick(record)">编辑用户信息</a-button>
        <a-modal v-model:visible="user_visible_var" @ok="user_handleOk" @cancel="user_handleCancel">
          <template #title>
            Title
          </template>
          <div>显示的是编辑用户信息</div>
        </a-modal>
      </template>
    </a-table>
  </div>
</template>

<script>
import { reactive, ref, getCurrentInstance } from 'vue';
export default {
  setup() {
    const classroom_visible_var = ref(false);

    const classroom_handleClick = () => {
      classroom_visible_var.value = true;
    };
    const classroom_handleOk = () => {
      classroom_visible_var.value = false;
    };
    const classroom_handleCancel = () => {
      classroom_visible_var.value = false;
    }
    const class_visible_var = ref(false);

    const class_handleClick = () => {
      class_visible_var.value = true;
    };
    const class_handleOk = () => {
      class_visible_var.value = false;
    };
    const class_handleCancel = () => {
      class_visible_var.value = false;
    }
    const user_visible_var = ref(false);

    const user_handleClick = () => {
      user_visible_var.value = true;
    };
    const user_handleOk = () => {
      user_visible_var.value = false;
    };
    const user_handleCancel = () => {
      user_visible_var.value = false;
    }
    const layout = ref('byclassrooms')
    const ispagination = true
    const classroom_columns = [
      {
        title: '名称',
        dataIndex: 'name',
      },
      {
        title: '容量',
        dataIndex: 'capacity',
      },
      {
        title: '地点',
        dataIndex: 'place',
      },
      {
        title: '操作',
        slotName: 'optional',
      },
    ];
    const classroom_data = reactive([
      {
        name: '主M201',
        capacity: 200,
        place: '主M201',
      },
      {
        name: '主M202',
        capacity: 150,
        place: '主M202',
      },
      {
        name: '主M203',
        capacity: 100,
        place: '主M203',
      },
    ]);
    const class_columns = [
      {
        title: '名称',
        dataIndex: 'name',
      },
      {
        title: '最大容量',
        dataIndex: 'max_capacity',
      },
      {
        title: '课时',
        dataIndex: 'course_hour',
      },
      {
        title: '类型',
        dataIndex: 'type',
      },
      {
        title: '简介',
        dataIndex: 'introduction',
      },
      {
        title: '学分',
        dataIndex: 'score',
      },
      {
        title: '操作',
        slotName: 'optional',
      },
    ];
    const class_data = reactive([
      {
        name:'数学分析',
        max_capacity:30,
        course_hour:16,
        type: '基础课程',
        introduction: '介绍高等数学的相关课程',
        score: 1,
      },
      {
        name:'数学分析',
        max_capacity:30,
        course_hour:16,
        type: '基础课程',
        introduction: '介绍高等数学的相关课程',
        score: 1,
      },
      {
        name:'数学分析',
        max_capacity:30,
        course_hour:16,
        type: '基础课程',
        introduction: '介绍高等数学的相关课程',
        score: 1,
      },
      {
        name:'数学分析',
        max_capacity:30,
        course_hour:16,
        type: '基础课程',
        introduction: '介绍高等数学的相关课程',
        score: 1,
      },
      {
        name:'数学分析',
        max_capacity:30,
        course_hour:16,
        type: '基础课程',
        introduction: '介绍高等数学的相关课程',
        score: 1,
      },
    ]);
    const user_columns = [
      {
        title: '用户名',
        dataIndex: 'user_name',
      },
      {
        title: '类型',
        dataIndex: 'type',
      },
      {
        title: '姓名',
        dataIndex: 'name',
      },
      {
        title: '性别',
        dataIndex: 'sex',
      },
      {
        title: '学号/工号',
        dataIndex: 'id',
      },
      {
        title: '职称',
        dataIndex: 'profession_title',
      },
      {
        title: '专业',
        dataIndex: 'major',
      },
      {
        title: '班级',
        dataIndex: 'class',
      },
      {
        title: '操作',
        slotName: 'optional',
      },
    ];
    const user_data = reactive([
      {
        user_name:'wjxchn',
        type:'学生',
        name:'王嘉鑫',
        sex: '男',
        id: 'SY2206216',
        major: '软件工程',
        class: 'SY22063'
      },
      {
        user_name:'hzt',
        type:'教师',
        name:'何智涛',
        sex: '男',
        id: '05163',
        profession_title: '讲师',
      },
      {
        user_name:'admin',
        type:'管理员',
      },
    ])
    const {proxy} = getCurrentInstance()
    const getClassroomData = function(){
      proxy.$http.get("getclassroom/").then((res) => {
        console.log(res);
      }) .catch((res) => {
        console.log(res);
      });
    }
    getClassroomData()
    return {
      classroom_columns,
      class_columns,
      user_columns,
      classroom_data,
      class_data,
      user_data,
      layout,
      ispagination,
      classroom_visible_var,
      classroom_handleClick,
      classroom_handleOk,
      classroom_handleCancel,
      class_visible_var,
      class_handleClick,
      class_handleOk,
      class_handleCancel,
      user_visible_var,
      user_handleClick,
      user_handleOk,
      user_handleCancel,
    }
  },
}
</script>
<style scoped>
.govern-data{
  padding-left:100px;
  padding-right: 100px;
  padding-top: 100px;
  padding-bottom: 100px;
}
</style>
