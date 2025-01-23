export default {
    template: `
    <div class="row">
        <div class="col">
            <img src="http://localhost:5000/static/images/home.png" style="width:100%; height :100vh; background-size: cover;"/>
        </div>
        <div class="col" style="text-align: center;align-items:center">
            <a class="navbar-brand" href="/">
                <img src="http://localhost:5000/static/images/logo.png" alt="Learnix" height="200" style="margin-top:3vh;">
            </a>
            <div style="text-align: center;margin-bottom:8vh;align-items:center">
                <br>
                <div style="margin: auto; color: red;">
                    {{ error }}
                </div>
                <br>
                <div class="form-floating" style="width: 75%;margin: auto">
                    <input type="text" class="form-control" name="name" placeholder="Name" 
                            v-model='cred.name' autofocus>
                    <label for="name">Name</label>
                </div>
                <br>
                <div class="form-floating" style="width: 75%;margin: auto">
                    <input type="email" class="form-control" name="email" placeholder="Email address" 
                            v-model='cred.email' autofocus>
                    <label for="email">Email address</label>
                </div>
                <br>
                <div class="form-floating" style="width: 75%;margin: auto">
                    <input type="password" class="form-control" name="password" placeholder="Password" 
                        v-model='cred.password' @input="checkPasswordsMatch">
                    <label for="password">Password</label>
                </div>
                <br>
                <div class="form-floating" style="width: 75%;margin: auto">
                    <input type="password" class="form-control" name="cnfpassword" placeholder="Confirm Password" 
                        v-model='cnfpassword' @input="checkPasswordsMatch">
                    <label for="cnfpassword">Confirm Password</label>
                </div>
                <br>   
                <button type="submit" class="btn btn-success" style="background-color: #015668;" 
                        :disabled="cred.name === null || cred.name === '' ||
                                    cred.email === null || cred.email === '' || 
                                    cred.password === null || cred.password === '' || cred.password !== cnfpassword"
                        @click='register'>Register</button> 
                <br><br>
                <router-link to="/">Existing User? Login!</router-link>
            </div>    
        </div>
    </div>
    `,
    data() {
        return {
            cred: {
                name: null,
                email: null,
                password: null                
            },
            cnfpassword: null,
            error: null
        }
    },
    methods: {
        checkPasswordsMatch(){
            if (this.cred.password === this.cnfpassword)
                this.error = null
            else
                this.error = 'Passwords do not match'
        },
        async register() {
            const res = await fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.cred),
            })
            const data = await res.json()
            if (res.ok) {
                alert(data.message)
                this.$router.push('/')
            }
            else{
                this.error = data.message
            }
        }
    }
}