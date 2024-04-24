import {reactive} from "vue";
import http from "../utils/https";
import {ElMessage} from "element-plus";

const user = reactive({
    account: "", // 登录账号/手机号/邮箱
    password: "", // 登录密码
    re_password: "", // 确认密码
    login_type: 0, // 登录方式，0，密码登录，1，短信登录
    remember: false,  // 是否记住登录状态
    code: "", // 短信验证码
    mobile: "", // 手机号
    sms_btn_text: "点击获取验证码", // 短信按钮提示
    is_send: false,  // 短信发送的标记
    sms_interval: 60,// 间隔时间
    interval: null,  // 定时器的标记
    avatar: "",
    sms_login(res) {
        res.val_mobile = this.mobile
        res.sms_code = this.code
        return http.post("/users/sms_login/", res);
    },
    login(res) {
        res.username = this.account
        res.password = this.password
        return http.post("/users/login/", res);
    },
    check_mobile() {
        // 验证手机号
        return http.get(`/users/mobile/${this.mobile}/`)
    },
    register(data) {
        data.mobile = this.mobile
        data.re_password = this.re_password
        data.password = this.password
        data.sms_code = this.code
        // 用户注册请求
        return http.post("/users/register/", data)
    },
    get_sms_code() {
        return http.get(`/users/sms/${this.mobile}/`)
    },
    // 发送短信
    send_sms(){
        if (!/1[3-9]\d{9}/.test(user.mobile)) {
            ElMessage.error("手机号格式有误！")
            return false
        }
        if (user.is_send) {
            ElMessage.error("短信发送过于频繁！")
            return false
        }
        let time = user.sms_interval;
        user.get_sms_code().then(resp => {
            ElMessage.success("短信发送中，请留意您的手机！");
            user.is_send = true;
            clearInterval(user.interval);
            user.interval = setInterval(() => {
                if (time < 1) {
                    user.is_send = false
                    user.sms_btn_text = "点击获取验证码"
                } else {
                    time -= 1;
                    user.sms_btn_text = `${time}秒后重新获取验证码`;
                }
            }, 1000);
        }).catch(error => {
            ElMessage.error(error?.response?.data?.errmsg);
            time = error?.response?.data?.interval;
            clearInterval(user.interval);
            user.interval = setInterval(() => {
                if (time < 1) {
                    // 退出短信发送的冷却状态
                    user.is_send = false
                    user.sms_btn_text = "点击获取验证码"
                } else {
                    time -= 1;
                    user.sms_btn_text = `${time}秒后重新获取`;
                }
            }, 1000)
        })
    }
})

export default user;