import Register from '/static/components/Register.js'
import Login from '/static/components/Login.js'
import Userdashboard from '/static/components/Userdashboard.js'
import CourseContents from '/static/components/CourseContents.js'

const routes = [
    { path: '/register', component: Register , name: 'Register'},
    { path: '/', component: Login, name: 'Login' },
    { path: '/userdashboard', component: Userdashboard },
    { path: '/coursecontents', component: CourseContents },
]

export default new VueRouter({
    routes,
})