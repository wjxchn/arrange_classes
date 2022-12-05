import { createRouter, createWebHistory } from 'vue-router'
import routes from './routes'

// 通过 createRouter 创建路由实例
// history: 用于路由实现历史记录, 
// 参数值为历史记录模式, 通过使用官方为我们提供方法(createWebHistory)即可。
const router = createRouter({
    // createWebHistory 创建history路由模式
	// createWebHashHistory 创建hash路由模式
	// createMemoryHistory 创建基于内存的历史记录
    history: createWebHistory(),
    // 路由表
    routes
})

export default router
