export default {
    template: `
    <div>
    <!-- Top nav bar -->
    <nav class="navbar bg-body-tertiary">
        <div class="container-fluid">
            <!-- Top left logo -->
            <a class="navbar-brand">    
                <img src="http://localhost:5000/static/images/logo.png" alt="Learnix" width="100" height="60">
            </a>
            <div class="text-center mx-auto">
                <span class="text-muted">
                    <span style="font-size: 24px">💡</span> {{ quoteText }}<em style="font-size: 16px"> – {{ quoteAuthor }}</em>
                </span>
            </div>
            <div>
                <a style="display: inline-block; margin-right:30px">Ask Lumi</a>
                <li class="nav-item dropdown" style="list-style-type: none;display: inline-block">
                        <a class="nav-link dropdown-toggle" id="userMenu" data-bs-toggle="dropdown" aria-expanded="false">
                            Welcome, {{name}}
                        </a>
                        <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userMenu">
                            <li><a class="dropdown-item">Edit Profile</a></li>
                            <li><a class="dropdown-item">Change Password</a></li>
                            <li><a class="dropdown-item" @click='logout'>Logout</a></li>
                        </ul>
                </li>
            </div>
        </div>
    </nav>
    <div class="row" style="width:100%">
        <div class="col-2" style="width: 20%; padding-right: 0px;" v-if="role=='user'">
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
    </div>              
    `,
    data() {
        return {
            role: JSON.parse(localStorage.getItem('user')).role,
            name: JSON.parse(localStorage.getItem('user')).name,
            weeks: [],
            activeWeek: 1, // Tracks which week content is open by default
            lectures: [],
            quotes: [
                "Education is the most powerful weapon you can use to change the world.  –  Nelson Mandela",
                "The beautiful thing about learning is that no one can take it away from you.  –  B.B. King",
                "Success is no accident. It is hard work, perseverance, and learning.  –  Pelé",
                "Learning never exhausts the mind.  –  Leonardo da Vinci",
                "An investment in knowledge pays the best interest.  –  Benjamin Franklin",
                "The roots of education are bitter, but the fruit is sweet.  –  Aristotle",
                "Education is not preparation for life; education is life itself.  –  John Dewey",
                "Wisdom is not a product of schooling but of the lifelong attempt to acquire it.  –  Albert Einstein",
                "Develop a passion for learning. If you do, you will never cease to grow.  –  Anthony J. D’Angelo",
                "The purpose of education is to replace an empty mind with an open one.  –  Malcolm Forbes",
              ],
            quoteText: "",
            quoteAuthor: ""
        }
    },
    mounted() {    
        const randomQuote = this.quotes[Math.floor(Math.random() * this.quotes.length)];
        const splitQuote = randomQuote.split("–");
        this.quoteText = splitQuote[0].trim(); // Extract the quote text
        this.quoteAuthor = splitQuote[1].trim(); // Extract the author's name

        // Fetch all lectures
        fetch('/get_all_lectures') 
          .then(response => response.json())
          .then(data => {
            this.lectures = data;
            this.weeks = new Set([...this.lectures
                .map(lecture => lecture.weeknumber) // Extract week numbers
                .sort((a, b) => a - b) // Sort in ascending order
              ]);
          });
    },
    methods: {
        profile() {
            this.$router.push("/profile")
        },
        changepwd() {
            this.$router.push("/changepwd")
        },
        logout() {
            localStorage.clear()
            this.$router.push("/")
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