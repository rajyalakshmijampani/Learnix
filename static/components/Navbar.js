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
    <slot></slot>
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