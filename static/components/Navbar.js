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
            <li class="nav-item dropdown" style="list-style-type: none;">
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
    </nav>
     
    </div>              
    `,
    data() {
        return {
            role: JSON.parse(localStorage.getItem('user')).role,
            name: JSON.parse(localStorage.getItem('user')).name,
            message: null,
            message_type: null,
        }
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
    }
}