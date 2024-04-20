import {reactive} from "vue";
import http from "../utils/https";

const user = reactive({
    account:"",
    password:"",
    login_type:0,
    remember:false,
    code:"",
    mobile:"",
    login(){
        return http.post("/users/login/", {"username":this.account,"password":this.account});
    }
})

export default user;