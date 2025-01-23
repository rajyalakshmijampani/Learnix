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
        <div class="col-2" style="width: 15%; padding-right: 0px;" v-if="role=='user'">
            <div style="margin-left:5%"> 
                <h5 style="color: #015668;margin-top: 60px;margin-bottom: 40px;text-align:center">Course Contents</h5>
                <div class="accordion">
                    <div class="accordion-item" v-for="(number, index) in weeks" :key="index">
                        <h2 class="accordion-header" :id="'heading' + index">
                            <button class="accordion-button" type="button" 
                                    :data-bs-toggle="'collapse'"
                                    :class="{ 'collapsed': activeIndex !== index }"
                                    :data-bs-target="'#collapse' + index" 
                                    :aria-expanded="activeIndex === index"
                                    :aria-controls="'collapse' + index"
                                    @click="activeIndex = activeIndex === index ? -1 : index">
                                Week {{ index + 1 }}
                            </button>
                        </h2>
                        <div class="aaccordion-collapse collapse" 
                            :class="{ 'show': activeIndex === index }"
                            :id="'collapse' + index" 
                            data-bs-parent="#accordionExample">
                            <div class="accordion-body">
                                <strong>This is the content for Week {{ index + 1 }}.</strong>
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
            message: null,
            message_type: null,
            weeks: [],
            activeIndex: -1, // Tracks which week content is open by default
            lectures: [],
        }
    },
    mounted() {
        // Fetch distinct week numbers
        fetch('/get_distinct_weeknumbers') 
          .then(response => response.json())
          .then(data => {
            this.weeks = data;
          });
    
        // Fetch all lectures
        fetch('/get_all_lectures') 
          .then(response => response.json())
          .then(data => {
            this.lectures = data;
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
    }
}