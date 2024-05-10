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
    },
    {
        meta: {
            title: "luffy2.0-用户注册",
            keepAlive: true
        },
        path: '/register',
        name: "Register",            // 路由名称
        component: () => import("../views/Register.vue"),         // uri绑定的组件页面
    },
    {
        meta: {
            title: "luffy-个人中心",
            keepalive: true,
            authorization: true
        },
        path: '/user',
        name: 'User',
        component: () => import("../views/User.vue")
    },
    {
        meta: {
            title: "luffy2.0-课程列表",
            keepAlive: true
        },
        path: '/project',
        name: "Course",            // 路由名称
        component: () => import("../views/Course.vue"),         // uri绑定的组件页面
    },
    {
        meta:{
            title: "luffy2.0-课程详情",
            keepAlive: true
        },
        path: '/project/:id',     // :id vue的路径参数，代表了课程的ID
        name: "Info",
        component: ()=> import("../views/Info.vue"),
    },
    {
      meta:{
        title: "luffy2.0-购物车",
        keepAlive: true
      },
      path: '/cart',
      name: "Cart",
      component: ()=> import("../views/Cart.vue"),
    },
    {
      meta:{
        title: "确认下单",
        keepAlive: true
      },
      path: '/order',
      name: "Order",
      component: ()=> import("../views/Order.vue"),
    },
    {
      meta:{
        title: "支付成功",
        keepAlive: true
      },
      path: '/alipay',
      name: "PaySuccess",
      component: ()=> import("../views/AliPaySuccess.vue"),
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    document.title = to.meta.title
    if (to.meta.authorization && !store.getters.getUserInfo) {
        next({"name": "Login"})
    } else {
        next()
    }
})


export default router