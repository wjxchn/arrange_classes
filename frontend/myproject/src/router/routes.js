const routes = [
    {
        name: 'homepage',
        path: '/',
        component: () => import('../view/HomePage.vue')
        // 注意不能使用 "@/view/index.vue"
        // vite 不识别的, 会出现找不到模块的情况
    },
    {
        name: 'showresult',
        path: '/showresult',
        component: () => import('../view/ShowResult.vue')
        // 注意不能使用 "@/view/index.vue"
        // vite 不识别的, 会出现找不到模块的情况
    },
    {
        name: 'governdata',
        path: '/governdata',
        component: () => import('../view/GovernData.vue')
    },
    {
        name: 'aboutus',
        path: '/aboutus',
        component: () => import('../view/AboutUs.vue')
    },
]

export default routes