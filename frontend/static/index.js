import router from "./router.js"
import Navbar from "./components/Navbar.js"

// Navigation Guard

router.beforeEach((to,from,next) => {
    if (to.name !== 'Login' && to.name !== 'Register' && !JSON.parse(localStorage.getItem('user')).token) next({name:'Login'})
    else next()
})

new Vue({
    el: "#app",
    template: `
    <div>
        <router-view/>
    </div>
    `,
    router,
    components: {
        Navbar,     //registering local component
    },
})