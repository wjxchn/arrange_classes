<template>
  <div class="govern-data">
    <a-space direction="vertical" size="large" :style="{width: '600px'}" style="margin-bottom: 60px;">
      <a-radio-group v-model="layout" type="button">
        <a-radio value="byclassrooms">管理教室信息</a-radio>
        <a-radio value="byclasses">管理课程信息</a-radio>
        <a-radio value="byusers">管理用户信息</a-radio>
      </a-radio-group>
    </a-space>
    <a-table v-show="layout=='byclassrooms'" :columns="classroom_columns" :data="classroom_data" :pagination="ispagination"/>
    <a-table v-show="layout=='byclasses'" :columns="class_columns" :data="class_data" :pagination="ispagination"/>
    <a-table v-show="layout=='byusers'" :columns="user_columns" :data="user_data" :pagination="ispagination"/>
  </div>
</template>

<script>
import { reactive, ref } from 'vue';

export default {
  setup() {
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
    const class_data = reactive([
      {
        monday:'1',
        tuesday:'2',
        wednesday:'3',
        thursday: '4',
        friday: '5',
        saturday: '6',
        sunday: '7'
      },
      {
        monday:'1',
        tuesday:'2',
        wednesday:'3',
        thursday: '4',
        friday: '5',
        saturday: '6',
        sunday: '7'
      },
      {
        monday:'1',
        tuesday:'2',
        wednesday:'3',
        thursday: '4',
        friday: '5',
        saturday: '6',
        sunday: '7'
      },
      {
        monday:'1',
        tuesday:'2',
        wednesday:'3',
        thursday: '4',
        friday: '5',
        saturday: '6',
        sunday: '7'
      },
      {
        monday:'1',
        tuesday:'2',
        wednesday:'3',
        thursday: '4',
        friday: '5',
        saturday: '6',
        sunday: '7'
      },
      {
        monday:'1',
        tuesday:'2',
        wednesday:'3',
        thursday: '4',
        friday: '5',
        saturday: '6',
        sunday: '7'
      },
      {
        monday:'1',
        tuesday:'2',
        wednesday:'3',
        thursday: '4',
        friday: '5',
        saturday: '6',
        sunday: '7'
      },
      {
        monday:'1',
        tuesday:'2',
        wednesday:'3',
        thursday: '4',
        friday: '5',
        saturday: '6',
        sunday: '7'
      },
      {
        monday:'1',
        tuesday:'2',
        wednesday:'3',
        thursday: '4',
        friday: '5',
        saturday: '6',
        sunday: '7'
      },
      {
        monday:'1',
        tuesday:'2',
        wednesday:'3',
        thursday: '4',
        friday: '5',
        saturday: '6',
        sunday: '7'
      },
      {
        monday:'1',
        tuesday:'2',
        wednesday:'3',
        thursday: '4',
        friday: '5',
        saturday: '6',
        sunday: '7'
      },
      {
        monday:'1',
        tuesday:'2',
        wednesday:'3',
        thursday: '4',
        friday: '5',
        saturday: '6',
        sunday: '7'
      },
      {
        monday:'1',
        tuesday:'2',
        wednesday:'3',
        thursday: '4',
        friday: '5',
        saturday: '6',
        sunday: '7'
      },
      {
        monday:'1',
        tuesday:'2',
        wednesday:'3',
        thursday: '4',
        friday: '5',
        saturday: '6',
        sunday: '7'
      },
    ]);
    const user_columns = [
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
    const user_data = reactive([
      {
        monday:'1',
        tuesday:'2',
        wednesday:'3',
        thursday: '4',
        friday: '5',
        saturday: '6',
        sunday: '7'
      },
      {
        monday:'1',
        tuesday:'2',
        wednesday:'3',
        thursday: '4',
        friday: '5',
        saturday: '6',
        sunday: '7'
      },
      {
        monday:'1',
        tuesday:'2',
        wednesday:'3',
        thursday: '4',
        friday: '5',
        saturday: '6',
        sunday: '7'
      },
      {
        monday:'1',
        tuesday:'2',
        wednesday:'3',
        thursday: '4',
        friday: '5',
        saturday: '6',
        sunday: '7'
      },
      {
        monday:'1',
        tuesday:'2',
        wednesday:'3',
        thursday: '4',
        friday: '5',
        saturday: '6',
        sunday: '7'
      },
      {
        monday:'1',
        tuesday:'2',
        wednesday:'3',
        thursday: '4',
        friday: '5',
        saturday: '6',
        sunday: '7'
      },
      {
        monday:'1',
        tuesday:'2',
        wednesday:'3',
        thursday: '4',
        friday: '5',
        saturday: '6',
        sunday: '7'
      },
      {
        monday:'1',
        tuesday:'2',
        wednesday:'3',
        thursday: '4',
        friday: '5',
        saturday: '6',
        sunday: '7'
      },
      {
        monday:'1',
        tuesday:'2',
        wednesday:'3',
        thursday: '4',
        friday: '5',
        saturday: '6',
        sunday: '7'
      },
      {
        monday:'1',
        tuesday:'2',
        wednesday:'3',
        thursday: '4',
        friday: '5',
        saturday: '6',
        sunday: '7'
      },
      {
        monday:'1',
        tuesday:'2',
        wednesday:'3',
        thursday: '4',
        friday: '5',
        saturday: '6',
        sunday: '7'
      },
      {
        monday:'1',
        tuesday:'2',
        wednesday:'3',
        thursday: '4',
        friday: '5',
        saturday: '6',
        sunday: '7'
      },
      {
        monday:'1',
        tuesday:'2',
        wednesday:'3',
        thursday: '4',
        friday: '5',
        saturday: '6',
        sunday: '7'
      },
      {
        monday:'1',
        tuesday:'2',
        wednesday:'3',
        thursday: '4',
        friday: '5',
        saturday: '6',
        sunday: '7'
      },
    ]);
    return {
      classroom_columns,
      class_columns,
      user_columns,
      classroom_data,
      class_data,
      user_data,
      layout,
      ispagination,
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
