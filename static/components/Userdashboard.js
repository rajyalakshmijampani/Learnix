import Navbar from "/static/components/Navbar.js"

export default {
    template: `
    <Navbar>
        <div class="col">
            <div class="row">
                
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
            error: null,
        }
    },
    methods: {
        clearMessage() {
            this.error = null
        },
    }
}