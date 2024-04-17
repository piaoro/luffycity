import {createRouter, createWebHistory} from 'vue-router'

const routes = [
    {
        meta: {
            title: "luffy-首页",
            keepalive: true
        },
        path: '/',
        name: 'home',
        component: () => import("../views/Home.vue")
    },
    {
        meta: {
            title: "luffy-y用户登录",
            keepalive: true
        },
        path: '/login',
        name: 'Login',
        component: () => import("../views/Login.vue")
    }
]

const router = createRouter({
    history:createWebHistory(),
    routes,
});


export default router