import http from "../utils/https.js";
import {reactive,ref} from "vue"

const banner = reactive({
    banner_list:[],
    get_banner_list(){
        return http.get("/home/banner/")
    }
});

export default banner;