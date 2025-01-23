import Navbar from "/static/components/Navbar.js"

export default {
    template: `
    <Navbar>
        <div class="col">
            <div class="row" style="margin : 2vh 0 2vh 0; width:30%; height: 5vh;align-items: center;">
                <div style="padding-left: 0;color:red;" v-if="error">
                    {{ error }}
                    <button class="btn-close" style="float: inline-end;" @click="clearMessage"></button>
                </div>
            </div>
            <div class="row mb-3">
                <div>
                    <b-tabs content-class="mt-3" pills card fill >
                        <b-tab title="My Holdings" active>
                            <h4 style="color: #015668;margin-left:2%;margin-top:3%"> {{this.user_current_books.issues.length}} book(s) in your account currently !! </h4>
                            <b-container style="margin-top:3%">
                                <b-row>
                                    <b-col v-for="(book,index) in paginatedIssues" :key="index" cols="3" class="mb-3">
                                        <Book :book="book" :page='location'/>
                                    </b-col>
                                </b-row>
                                <p style="margin-top:5%;margin-left:42%">Showing 4 results per page</p>
                                <b-pagination v-model="currentPage" :total-rows="totalIssues" :per-page="booksPerPage" style="justify-content:center"/>
                            </b-container>
                        </b-tab>
                        <b-tab title="My Purchases">
                            <h4 style="color: #015668;margin-left:2%;margin-top:3%"> {{this.user_current_books.purchases.length}} book(s) purchased !! </h4>
                            <b-container style="margin-top:3%">
                                <b-row>
                                    <b-col v-for="(book,index) in paginatedPurchases" :key="index" cols="3" class="mb-3">
                                        <Book :book="book"/>
                                    </b-col>
                                </b-row>
                                <p style="margin-top:5%;margin-left:42%">Showing 4 results per page</p>
                                <b-pagination v-model="currentPage" :total-rows="totalPurchases" :per-page="booksPerPage" style="justify-content:center"/>
                            </b-container>
                        </b-tab>
                        <b-tab title="Pending Requests">
                            <h4 style="color: #015668;margin-left:2%;margin-top:3%"> {{this.user_current_books.requests.length}} request(s) pending for admin's approval !! </h4>
                            <b-container style="margin-top:3%">
                                <b-row>
                                    <b-col v-for="(book,index) in paginatedRequests" :key="index" cols="3" class="mb-3">
                                        <Book :book="book"/>
                                    </b-col>
                                </b-row>
                                <p style="margin-top:5%;margin-left:42%">Showing 4 results per page</p>
                                <b-pagination v-model="currentPage" :total-rows="totalRequests" :per-page="booksPerPage" style="justify-content:center"/>
                            </b-container>
                        </b-tab>
                        
                    </b-tabs>
                </div>
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
            user_current_books: {'issues':[],'requests':[],'purchases':[]},
            error: null,
            location: 'user_dashboard',
            currentPage: 1,
            booksPerPage: 4,
        }
    },
    computed: {
        totalIssues() {
            return this.user_current_books.issues.length;
          },
          paginatedIssues() {
            const start = (this.currentPage - 1) * this.booksPerPage;
            const end = start + this.booksPerPage;
            return this.user_current_books.issues.slice(start, end);
          },
        totalPurchases() {
            return this.user_current_books.purchases.length;
          },
          paginatedPurchases() {
            const start = (this.currentPage - 1) * this.booksPerPage;
            const end = start + this.booksPerPage;
            return this.user_current_books.purchases.slice(start, end);
          },
        totalRequests() {
          return this.user_current_books.requests.length;
        },
        paginatedRequests() {
          const start = (this.currentPage - 1) * this.booksPerPage;
          const end = start + this.booksPerPage;
          return this.user_current_books.requests.slice(start, end);
        }
      },
    created(){
        this.userBooks()
    },
    methods: {
        clearMessage() {
            this.error = null
        },
        async userBooks(){
            const res = await fetch(`/user/${this.user_id}/currentbooks`, {
                headers: {
                    "Authentication-Token": this.token
                    }
                })
            if (res.ok) {
                const data = await res.json()
                this.user_current_books = data
                }
        },
    }
}