import {createStore} from 'vuex';
import createPersistedState from "vuex-persistedstate"

const store = createStore({
    plugins:[createPersistedState()],
    state(){
        return{
            user:{

            },
            cart_total: 0, // 购物车中的商品数量，默认为0
        }
    },
    getters:{
        getUserInfo(state){
            let now = parseInt((new Date() - 0)/1000);
            if(state.user.exp === undefined){
                state.user = {}
                localStorage.token = null
                sessionStorage.token = null
                return null
            }
            if(parseInt(state.user.exp) < now){
                state.user = {}
                localStorage.token = null
                sessionStorage.token = null
                return null
            }
            return state.user;
        }
    },
    mutations:{
        login(state,user){
            state.user = user
        },
        logout(state){
            state.user = {}
            localStorage.token = null;
            sessionStorage.token = null;
        },
        cart_total(state, total) {
            // 设置商品数量的总数
            state.cart_total = total
        },
    }
})

export default store;