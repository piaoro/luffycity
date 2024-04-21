import {createStore} from 'vuex';
import createPersistedState from "vuex-persistedstate"

const store = createStore({
    plugins:[createPersistedState()],
    state(){
        return{
            user:{

            }
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
        }
    }
})

export default store;