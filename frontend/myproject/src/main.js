import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.js'
import axios from "axios";
import ArcoVue from '@arco-design/web-vue';
import '@arco-design/web-vue/dist/arco.css';
const app = createApp(App)
app.use(router)
app.use(ArcoVue)
app.mount('#app')

axios.defaults.baseURL = "/api";
app.config.globalProperties.$http = axios