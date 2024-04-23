import {reactive} from "vue";
import http from "../utils/https";

const user = reactive({
    account: "",
    password: "",
    login_type: 0,
    remember: false,
    code: "",
    mobile: "",
    login(res) {
        return http.post("/users/login/", {
            "ticket": res.ticket,
            "randstr": res.randstr,
            "username": this.account,
            "password": this.password
        });
    },
    check_mobile(){
        // 验证手机号
        return http.get(`/users/mobile/${this.mobile}/`)
    }
})

export default user;