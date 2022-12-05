const routes = [
    {
        name: 'index',
        path: '/index',
        component: () => import('../view/IndexView.vue')
        // 注意不能使用 "@/view/index.vue"
        // vite 不识别的, 会出现找不到模块的情况
    },
    {
        name: 'details',
        path: '/details',
        component: () => import('../view/DetailsView.vue')
    },
    {
        name: 'helloworld',
        path: '/helloworld',
        component: () => import('../components/HelloWorld.vue')
    },
]

export default routes