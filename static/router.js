import Register from '/static/components/Register.js'
import Login from '/static/components/Login.js'
import Userdashboard from '/static/components/Userdashboard.js'

const routes = [
    { path: '/register', component: Register , name: 'Register'},
    { path: '/', component: Login, name: 'Login' },
    { path: '/userdashboard', component: Userdashboard },
]

export default new VueRouter({
    routes,
})