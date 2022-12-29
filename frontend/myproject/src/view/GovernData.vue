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
      <template #name-filter="{ filterValue, setFilterValue, handleFilterConfirm, handleFilterReset}">
        <div class="custom-filter">
          <a-space direction="vertical">
            <a-input :model-value="filterValue[0]" @input="(value)=>setFilterValue([value])" />
            <div class="custom-filter-footer">
              <a-button @click="handleFilterConfirm">Confirm</a-button>
              <a-button @click="handleFilterReset">Reset</a-button>
            </div>
          </a-space>
        </div>
      </template>
      <template #optional="{ record }">
        <a-button @click="classroom_handleClick(record)">编辑教室信息</a-button>
        <a-modal v-model:visible="classroom_visible_var" @ok="classroom_handleOk" @cancel="classroom_handleCancel">
          <template #title>
            Title
          </template>
          <div>显示的是编辑教室信息</div>
        </a-modal>
      </template>
      <template #delete_optional="{ record }">
        <a-button @click="classroom_delete_handleClick">删除教室信息</a-button>
        <a-modal v-model:visible="classroom_delete_visible_var" @ok="classroom_delete_handleOk(record)" @cancel="classroom_delete_handleCancel">
          <template #title>
            提示
          </template>
          <div>确认删除该教室吗？</div>
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
            提示
          </template>
          <div>编辑用户信息</div>
        </a-modal>
      </template>
    </a-table>
  </div>
</template>

<script>
import { reactive, ref, getCurrentInstance, h } from 'vue';
import { IconSearch } from '@arco-design/web-vue/es/icon';
import qs from 'qs'
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
    const classroom_delete_visible_var = ref(false);

    const classroom_delete_handleClick = () => {
      classroom_delete_visible_var.value = true;
    };
    const classroom_delete_handleOk = (record) => {
      console.log(record.id)
      deleteClassroomData(record.id)
      classroom_delete_visible_var.value = false;
    };
    const classroom_delete_handleCancel = () => {
      classroom_delete_visible_var.value = false;
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
        filterable: {
          filter: (value, record) => record.name.includes(value),
          slotName: 'name-filter',
          icon: () => h(IconSearch)
        }
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
        title: '编辑操作',
        slotName: 'optional',
      },
      {
        title: '删除操作',
        slotName: 'delete_optional',
      },
    ];
    const classroom_data = reactive([]);
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
    const class_data = reactive([]);
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
        dataIndex: 'work_id',
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
    const user_data = reactive([])
    const {proxy} = getCurrentInstance()
    const getClassroomData = function(){
      proxy.$http.get("getclassroom/").then((res) => {
        console.log(res);
        res.data.classrooms.forEach(element => {
          classroom_data.push({
            id: element.id,
            name: element.name,
            capacity: element.capacity,
            place: element.place
          })
        });
      }) .catch((res) => {
        console.log(res);
      });
    }
    const deleteClassroomData = function(id){
      console.log(id)
      let data={"id": id}
      proxy.$http.post("deleteclassroom/", qs.stringify({
        data
      })).then((res) => {
        console.log(res);
      }) .catch((res) => {
        console.log(res);
      });
    }
    getClassroomData()
    const getCourseData = function(){
      proxy.$http.get("getclass/").then((res) => {
        console.log(res);
        res.data.classrooms.forEach(element => {
          class_data.push({
            id: element.id,
            name: element.name,
            max_capacity: element.capacity,
            course_hour: element.hour,
            type: element.type,
            introduction: element.introduction,
            score: element.score,
          })
        });
      }) .catch((res) => {
        console.log(res);
      });
    }
    getCourseData()
    const getUserData = function(){
      proxy.$http.get("getuser/").then((res) => {
        console.log(res);
        res.data.users.forEach(element => {
          user_data.push({
            id: element.id,
            type: element.type,
            user_name: element.name
          })
        });
      }) .catch((res) => {
        console.log(res);
      });
    }
    getUserData()
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
      classroom_delete_visible_var,
      classroom_delete_handleClick,
      classroom_delete_handleOk,
      classroom_delete_handleCancel,
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
