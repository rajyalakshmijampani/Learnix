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
            <div class="col-2" style="margin-top:15px;width: 25%;">
                <div class="row mb-3" style="margin-top:50px;">
                    <h4 style="color: #015668;margin-left: 0px;margin-bottom: 25px">Announcements</h4>
                    <ul style="margin-left: 15px;">
                        <li style="font-size:18px;">
                            Course Cards for January 2025 Term Added to Your Dashboard. 
                            Use 
                                <a href="https://forms.study.iitm.ac.in/login" target="_blank" style="color: blue; text-decoration: underline;">
                                    this form
                                </a>
                            to report any issues.
                        </li>
                        <li style="font-size:18px;margin-top:25px">
                            On-campus workshops open for registration. 
                            Click
                            <a href="https://forms.study.iitm.ac.in/login" target="_blank" style="color: blue; text-decoration: underline;">
                                here
                            </a>
                            to know more.
                        </li>
                        <li style="font-size:18px;margin-top:25px">
                            Deadline for mandatory SCT extended till 1st April. 
                            Check out the process document
                            <a href="https://docs.google.com/document/d/13WhnPprgKrgMfJ-Ep9IJQdolharbkY4ucrrfQYVoe4c/pub" target="_blank" style="color: blue; text-decoration: underline;">
                                here.
                            </a>
                        </li>
                        <li style="font-size:18px;margin-top:25px">
                            Jan 2025 Grading document released.
                            <a href="https://docs.google.com/document/d/e/2PACX-1vRBH1NuM3ML6MH5wfL2xPiPsiXV0waKlUUEj6C7LrHrARNUsAEA1sT2r7IHcFKi8hvQ45gSrREnFiTT/pub?urp=gmail_link" target="_blank" style="color: blue; text-decoration: underline;">
                                Document Link.
                            </a>
                        </li>
                    </ul>
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
            formUrl: ''
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