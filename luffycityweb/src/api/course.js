import http from "../utils/https";
import {reactive, ref} from "vue"

const course = reactive({
    current_direction: 0,   // 当前选中的学习方向，0表示所有方向
    current_category: 0,    // 当前选中的课程分类，0表示不限分类
    direction_list: [],     // 学习方向列表
    category_list: [],      // 课程分类列表
    course_list: [],        // 课程列表数据
    ordering: "-id",       // 课程排序条件
    page: 1,               // 当前页码，默认为1
    size: 5,               // 当前页数据量
    count: 0,         // 课程信息列表的数量
    has_perv: false,  // 是否有上一页
    has_next: false,  // 是否有下一页
    timer: null,      // 课程相关数据的定时器
    text: "",
    course_id: null,  // 课程ID
    hot_word_list:[],   // 热搜词列表
    chapter_list: [], // 课程章节列表
    get_course_direction() {
        //  获取学习方向信息
        return http.get("/course/directions/")
    },
    get_course_category() {
        // 获取课程分类信息
        return http.get(`/course/category/${this.current_direction}/`)
    },
    get_course_list(param) {
        // 获取课程列表信息
        let params = {
            page: this.page,
            size: this.size,
        }
        if (this.ordering) {
            params.ordering = this.ordering;
        }
        if (parseInt(param) > 1) {
            return http.get(`/course/${this.current_direction}/${this.current_category}/`, {
                params
            })
        }
        return http.get(`/course/${this.current_direction}/${this.current_category}/`)

    },
    start_timer() {
        // 课程相关的优惠活动倒计时
        clearInterval(this.timer); // 保证整个页面只有一个倒计时对优惠活动的倒计时进行时间
        this.timer = setInterval(() => {
            this.course_list.forEach((course) => {
                // js的对象和python里面的字典/列表一样， 是属于引用类型的。所以修改了成员的值也会影响自身的。
                if (course.discount.expire && course.discount.expire > 0) {
                    // 时间不断自减
                    course.discount.expire--
                }
            })
        }, 1000)
    },
    search_course() {
        let params = {
            page: this.page,
            size: this.size,
            text: this.text,
        }
        if (this.ordering) {
            params['ordering'] = this.ordering
        }
        return http.get('/course/search/', {
            params,
        })
    },
    get_hot_word(){
        // 课程热搜关键字
        return http.get("/course/hot_word/")
    },
    info: {           // 课程详情信息
        teacher:{},   // 课程相关的老师信息
        discount:{    // 课程相关的折扣信息
          type: ""
        }
    },
    tabIndex: 1,      // 课程详情页中默认展示的课程信息的选项卡
    // 获取课程详情
    get_course(){
        return http.get(`/course/${this.course_id}`)
    },
    get_course_chapters(){
        // 获取指定课程的章节列表
        return http.get(`/course/${this.course_id}/chapters`)
    }
})

export default course;