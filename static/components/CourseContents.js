import Navbar from "/static/components/Navbar.js"

export default {
    template: `
    <Navbar>
        <div class="row" style="width:100%">
            <div class="col-2" style="width: 20%; padding-right: 0px;">
                <div style="margin-left:5%"> 
                    <h4 style="color: #015668;margin-top: 30px;margin-bottom: 30px;text-align:center">Course Contents</h4>
                    <div class="accordion" id="accordion">
                        <div class="accordion-item" v-for="weeknumber in weeks" :key="weeknumber">
                            <h2 class="accordion-header" :id="'heading' + weeknumber">
                                <button class="accordion-button" type="button" 
                                        :data-bs-toggle="'collapse'"
                                        :class="{ 'collapsed': activeWeek !== weeknumber }"
                                        :data-bs-target="'#collapse' + weeknumber" 
                                        :aria-expanded="activeWeek === weeknumber"
                                        :aria-controls="'collapse' + weeknumber"
                                        @click="activeWeek = activeWeek === weeknumber ? -1 : weeknumber">
                                    Week {{ weeknumber }}
                                </button>
                            </h2>
                            <div class="aaccordion-collapse collapse" 
                                :class="{ 'show': activeWeek === weeknumber }"
                                :id="'collapse' + weeknumber"
                                data-bs-parent="#accordion">
                                <div class="accordion-body" :style="{padding: '0'}">
                                    <ul class="list-group" :style="{margin: '0',borderRadius: '0'}">
                                        <li class="list-group-item" v-for="lecture in sortedLectures(weeknumber)" 
                                            :key="lecture.lecturenumber"
                                            :style="{ height: '65px', display: 'flex', alignItems: 'center',margin: '0'}">
                                            <a :href="lecture.link" target="_blank"
                                            :style="{ display: 'flex', alignItems: 'center',width: '100%', height: '100%', textDecoration: 'none', color: 'inherit' }">
                                                L{{ lecture.lecturenumber }} {{ lecture.title }}</a>
                                        </li>
                                        <li class="list-group-item"
                                            :style="{ height: '65px', display: 'flex', alignItems: 'center',margin: '0'}"
                                        > Mock Questions </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </Navbar>
    `,
    components:{
        Navbar
    },
    data() {
        return {
            token: JSON.parse(localStorage.getItem('user')).token,
            user_id: JSON.parse(localStorage.getItem('user')).id,
            user_name: JSON.parse(localStorage.getItem('user')).name,
            id: this.$route.query.id,
            error: null,
            weeks: [],
            activeWeek: 1, // Tracks which week content is open by default
            lectures: [],
        }
    },
    created(){
        this.fetchLectures()
    },
    methods: {
        clearMessage() {
            this.error = null
        },
        async fetchLectures(){
            const res = await fetch(`/get_all_lectures/${this.id}`, {
                headers: {
                    "Authentication-Token": this.token
                    }
                })
            if (res.ok) {
                const data = await res.json()
                this.lectures = data
                this.weeks = new Set([...this.lectures
                    .map(lecture => lecture.weeknumber) // Extract week numbers
                    .sort((a, b) => a - b) // Sort in ascending order
                  ]);
                }
        },
        toggleAccordion(index) {
            this.activeIndex = this.activeIndex === index ? null : index;
        },
        sortedLectures(week) {
            return this.lectures
              .filter(lecture => lecture.weeknumber === week)
              .sort((a, b) => a.lecturenumber - b.lecturenumber);
        },
    }
}