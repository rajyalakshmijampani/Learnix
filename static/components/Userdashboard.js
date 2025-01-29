import Navbar from "/static/components/Navbar.js"
import Course from "/static/components/Course.js"

export default {
    template: `
    <Navbar>
        <div class="row" style="width:100%">
            <div class="col-2" style="margin-top:15px;width: 75%; border-right: 2px solid black;">
                <div class="row mb-3" style="width: 75%; margin-top:30px; margin-left:30px">
                    <h2 style="color: #015668;margin-left: 0">My Current Courses</h2>
                </div>
                <div class="row" style="margin-top:30px;margin-left:30px;margin-right:10px">
                    <b-container>
                        <b-row cols="3">
                            <b-col v-for="course in user_courses" :key="course.id" class="mb-3">
                                <Course :course="course"/>
                            </b-col>
                        </b-row>
                    </b-container>
                </div>
            </div>
        </div>
    </Navbar>
    `,
    components:{
        Navbar,
        Course
    },
    data() {
        return {
            token: JSON.parse(localStorage.getItem('user')).token,
            user_id: JSON.parse(localStorage.getItem('user')).id,
            user_name: JSON.parse(localStorage.getItem('user')).name,
            user_courses: [],
            error: null,
        }
    },
    created(){
        this.userCourses()
    },
    methods: {
        clearMessage() {
            this.error = null
        },
        async userCourses(){
            const res = await fetch(`/user/${this.user_id}/currentcourses`, {
                headers: {
                    "Authentication-Token": this.token
                    }
                })
            if (res.ok) {
                const data = await res.json()
                this.user_courses = data
                }
        },
    }
}