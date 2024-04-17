import http from "../utils/https.js";
import {reactive,ref} from "vue"

const nav = reactive({
    header_nav_list:[],
    footer_nav_list:[],
    get_header_nav(){
        return http.get("/home/nav/header/")
    },
    get_footer_nav(){
        return http.get("/home/nav/footer/")
    },
});

export default nav;