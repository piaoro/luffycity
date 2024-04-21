import { createApp } from 'vue';
import App from './App.vue';
import 'element-plus/dist/index.css'
import router from "./router/index.js";
import store from "./store";


createApp(App).use(router).use(store).mount('#app')
