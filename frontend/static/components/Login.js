export default {
    template: `
    <div class="row">
        <div class="col">
            <img src="/static/images/home.png" style="width:100%; height :100vh; background-size: cover;"/>
        </div>
        <div class="col" style="text-align: center;align-items:center">
            <a class="navbar-brand" href="/">
                <img src="/static/images/logo.png" alt="Learnix" height="300" style="margin-top:3vh;">
            </a>
            <div style="text-align: center;margin-top:1vh; margin-bottom:8vh;align-items:center">
                <br>
                <div style="margin: auto; color: red;">
                    {{ error }}
                </div>
                <br>
                <div class="form-floating" style="width: 75%;margin: auto">
                    <input type="email" class="form-control" name="email" placeholder="Email address" 
                            v-model='cred.email' autofocus required>
                    <label for="email">Email address</label>
                </div>
                <br>
                <div class="form-floating" style="width: 75%;margin: auto">
                    <input type="password" class="form-control" name="password" 
                        placeholder="Password" v-model='cred.password' required>
                    <label for="password">Password</label>
                </div>
                <br>   
                <button class="btn btn-success" style="background-color: #015668;" 
                    :disabled="cred.email === null || cred.email === '' || 
                               cred.password === null || cred.password === ''" @click='login'>Login</button> 
                <br><br>
                <router-link to="/register">New User? Register!</router-link>
            </div>    
        </div>
    </div>
    `,
    data() {
        return {
            cred: {
                email: null,
                password: null,
            },
            error: this.$route.params.error
        }
    },
    methods: {
        async login() {
            const res = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.cred),
            })
            const data = await res.json()
            if (res.ok) {
                localStorage.setItem('user', JSON.stringify(data))
                this.$router.push({path : '/userdashboard'})
            }
            else{
                this.error = data.error
            }
        }
    }
}