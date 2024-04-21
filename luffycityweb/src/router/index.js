import {createRouter, createWebHistory} from 'vue-router'
import store from "../store";


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
    ,
    {
        meta: {
            title: "luffy-个人中心",
            keepalive: true,
            authorization:true
        },
        path: '/user',
        name: 'User',
        component: () => import("../views/User.vue")
    }
]

const router = createRouter({
    history:createWebHistory(),
    routes,
});

router.beforeEach((to,from,next)=>{
    document.title = to.meta.title
    if(to.meta.authorization && !store.getters.getUserInfo){
        next({"name":"Login"})
    }else{
        next()
    }
})


export default router