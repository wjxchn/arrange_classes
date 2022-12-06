<template>
    <div class="menu-demo">
        <a-menu mode="horizontal" :default-selected-keys="['1']">
        <a-menu-item key="0" style="padding: 0; marginRight: 38px; color: #A43525; font-weight:900; font-size:20px;" disabled>排课系统</a-menu-item>
        <a-menu-item key="1" @click="$router.push({path:'/'})">排课</a-menu-item>
        <a-menu-item key="2" @click="$router.push('showresult')">排课结果查看</a-menu-item>
        <a-menu-item key="3" @click="$router.push('governdata')">数据管理</a-menu-item>
        <a-menu-item key="4" @click="$router.push('aboutus')">关于</a-menu-item>
        </a-menu>
    </div>
</template>
<script>
export default{
}
</script>

<style scoped>
.menu-demo {
box-sizing: border-box;
width: 100%;
background-color: var(--color-neutral-2);
}
</style>