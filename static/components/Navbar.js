export default {
    template: `
    <div>
        <!-- Top nav bar -->
        <nav class="navbar bg-body-tertiary">
            <div class="container-fluid">
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
                    <li class="nav-item dropdown" style="list-style-type: none; display: inline-block">
                        <a class="nav-link dropdown-toggle" id="userMenu" data-bs-toggle="dropdown" aria-expanded="false">
                            Welcome, {{ name }}
                        </a>
                        <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userMenu">
                            <li><a class="dropdown-item" @click="openEditProfile">Edit Profile</a></li>
                            <li><a class="dropdown-item" @click="openChangePassword">Change Password</a></li>
                            <li><a class="dropdown-item" @click="logout">Logout</a></li>
                        </ul>
                    </li>
                </div>
            </div>
        </nav>

        <slot></slot>

        <!-- Edit Profile Dialog ------------------------------------------------------------------------------------------>
        <div v-if="showEditDialog" 
            :style="{
                position: 'fixed',
                top: '0',
                left: '0',
                width: '100%',
                height: '100%',
                background: 'rgba(0, 0, 0, 0.6)',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                zIndex: '1000',
                backdropFilter: 'blur(3px)'
            }">
            <div :style="{
                background: 'white',
                padding: '2rem',
                borderRadius: '12px',
                width: '450px',
                boxShadow: '0 4px 24px rgba(0, 0, 0, 0.15)',
                animation: 'slideIn 0.3s ease-out'
            }">
                <div :style="{
                    marginBottom: '1.5rem',
                    textAlign: 'center'
                }">
                    <h3 :style="{
                        fontSize: '1.5rem',
                        color: '#333',
                        margin: '0 0 0.5rem 0',
                        fontWeight: '600'
                    }">Edit Profile</h3>
                </div>

                <div :style="{
                    marginBottom: '1.25rem',
                    textAlign: 'left'
                }">
                    <label :style="{
                        display: 'block',
                        marginBottom: '0.5rem',
                        color: '#666',
                        fontSize: '0.9rem'
                    }">Old Name: {{ name }}</label>
                    <input 
                        v-model="newName" 
                        placeholder="Enter new name"
                        :style="{
                            width: '100%',
                            padding: '0.75rem',
                            border: '1px solid #ddd',
                            borderRadius: '6px',
                            fontSize: '1rem',
                            outline: 'none',
                            boxSizing: 'border-box'
                        }">
                </div>

                <div :style="{
                    marginBottom: '1.25rem',
                    textAlign: 'left'
                }">
                    <label :style="{
                        display: 'block',
                        marginBottom: '0.5rem',
                        color: '#666',
                        fontSize: '0.9rem'
                    }">Old Email: {{ email }}</label>
                    <input 
                        v-model="newEmail" 
                        placeholder="Enter new email"
                        :style="{
                            width: '100%',
                            padding: '0.75rem',
                            border: '1px solid #ddd',
                            borderRadius: '6px',
                            fontSize: '1rem',
                            outline: 'none',
                            boxSizing: 'border-box'
                        }">
                </div>

                <div :style="{
                    margin: '1.5rem 0',
                    textAlign: 'left'
                }">
                    <h4 :style="{
                        color: '#333',
                        marginBottom: '0.75rem',
                        fontSize: '1.1rem'
                    }">Registered Courses:</h4>
                    <ul :style="{
                        listStyle: 'none',
                        padding: '0',
                        margin: '0'
                    }">
                        <li 
                            v-for="course in registeredCourses" 
                            :key="course.id"
                            :style="{
                                padding: '0.5rem',
                                background: '#f8f9fa',
                                borderRadius: '4px',
                                marginBottom: '0.5rem',
                                color: '#495057',
                                fontSize: '0.95rem'
                            }">
                            {{ course.name }}
                        </li>
                    </ul>
                </div>

                <div :style="{
                    display: 'flex',
                    justifyContent: 'center',
                    gap: '1rem',
                    marginTop: '2rem'
                }">
                    <button 
                        @click="updateProfile"
                        :style="{
                            padding: '0.75rem 1.5rem',
                            borderRadius: '6px',
                            fontSize: '1rem',
                            cursor: 'pointer',
                            border: 'none',
                            background: '#007bff',
                            color: 'white',
                            transition: 'background 0.2s'
                        }">
                        Update
                    </button>
                    <button 
                        @click="closeEditProfile"
                        :style="{
                            padding: '0.75rem 1.5rem',
                            borderRadius: '6px',
                            fontSize: '1rem',
                            cursor: 'pointer',
                            border: 'none',
                            background: '#e9ecef',
                            color: '#495057',
                            transition: 'background 0.2s'
                        }">
                        Cancel
                    </button>
                </div>
            </div>
        </div>

        <style>
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        </style>

        <!-- Change Password Dialog ----------------------------------------------------------------------------------------->
        <div v-if="showChangePasswordDialog" 
            :style="{
                position: 'fixed',
                top: '0',
                left: '0',
                width: '100%',
                height: '100%',
                background: 'rgba(0, 0, 0, 0.6)',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                zIndex: '1000',
                backdropFilter: 'blur(3px)'
            }">
            <div :style="{
                background: 'white',
                padding: '2rem',
                borderRadius: '12px',
                width: '450px',
                boxShadow: '0 4px 24px rgba(0, 0, 0, 0.15)',
                animation: 'slideIn 0.3s ease-out'
            }">
                <div :style="{
                    marginBottom: '1.5rem',
                    textAlign: 'center'
                }">
                    <h3 :style="{
                        fontSize: '1.5rem',
                        color: '#333',
                        margin: '0 0 0.5rem 0',
                        fontWeight: '600'
                    }">Change Password</h3>
                </div>

                <div :style="{
                    marginBottom: '1.25rem',
                    textAlign: 'left'
                }">
                    <label :style="{
                        display: 'block',
                        marginBottom: '0.5rem',
                        color: '#666',
                        fontSize: '0.9rem'
                    }">Old Password:</label>
                    <input 
                        v-model="oldPassword" 
                        type="password"
                        placeholder="Enter old password"
                        :style="{
                            width: '100%',
                            padding: '0.75rem',
                            border: '1px solid #ddd',
                            borderRadius: '6px',
                            fontSize: '1rem',
                            outline: 'none',
                            boxSizing: 'border-box'
                        }">
                </div>

                <div :style="{
                    marginBottom: '1.25rem',
                    textAlign: 'left'
                }">
                    <label :style="{
                        display: 'block',
                        marginBottom: '0.5rem',
                        color: '#666',
                        fontSize: '0.9rem'
                    }">New Password:</label>
                    <input 
                        v-model="newPassword" 
                        type="password"
                        placeholder="Enter new password"
                        :style="{
                            width: '100%',
                            padding: '0.75rem',
                            border: '1px solid #ddd',
                            borderRadius: '6px',
                            fontSize: '1rem',
                            outline: 'none',
                            boxSizing: 'border-box'
                        }">
                </div>

                <div :style="{
                    marginBottom: '1.25rem',
                    textAlign: 'left'
                }">
                    <label :style="{
                        display: 'block',
                        marginBottom: '0.5rem',
                        color: '#666',
                        fontSize: '0.9rem'
                    }">Confirm New Password:</label>
                    <input 
                        v-model="confirmNewPassword" 
                        type="password"
                        placeholder="Confirm new password"
                        :style="{
                            width: '100%',
                            padding: '0.75rem',
                            border: '1px solid #ddd',
                            borderRadius: '6px',
                            fontSize: '1rem',
                            outline: 'none',
                            boxSizing: 'border-box'
                        }">
                </div>

                <div :style="{
                    display: 'flex',
                    justifyContent: 'center',
                    gap: '1rem',
                    marginTop: '2rem'
                }">
                    <button 
                        @click="changePassword"
                        :style="{
                            padding: '0.75rem 1.5rem',
                            borderRadius: '6px',
                            fontSize: '1rem',
                            cursor: 'pointer',
                            border: 'none',
                            background: '#007bff',
                            color: 'white',
                            transition: 'background 0.2s'
                        }">
                        Update Password
                    </button>
                    <button 
                        @click="closeChangePassword"
                        :style="{
                            padding: '0.75rem 1.5rem',
                            borderRadius: '6px',
                            fontSize: '1rem',
                            cursor: 'pointer',
                            border: 'none',
                            background: '#e9ecef',
                            color: '#495057',
                            transition: 'background 0.2s'
                        }">
                        Cancel
                    </button>
                </div>
            </div>
        </div>
    </div> 
    `,
    data() {
        return {
            role: JSON.parse(localStorage.getItem('user')).role,
            name: JSON.parse(localStorage.getItem('user')).name,
            email: JSON.parse(localStorage.getItem('user')).email,
            userId: JSON.parse(localStorage.getItem('user')).id,
            newName: "",
            newEmail: "",
            registeredCourses: [],
            showEditDialog: false,
            oldPassword: "",
            newPassword: "",
            confirmNewPassword: "",
            showChangePasswordDialog: false,
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
        this.quoteText = splitQuote[0].trim(); 
        this.quoteAuthor = splitQuote[1].trim(); 
    },
    methods: {
        profile() {
            this.$router.push("/profile");
        },
        changepwd() {
            this.$router.push("/changepwd");
        },
        logout() {
            localStorage.clear();
            this.$router.push("/");
        },
        openEditProfile() {
            console.log("Opening edit profile dialog...");
            this.showEditDialog = true;
            this.fetchRegisteredCourses();
        },        
        closeEditProfile() {
            this.showEditDialog = false;
            this.newName = "";
            this.newEmail = "";
        },
        fetchRegisteredCourses() {
            fetch(`/user/${this.userId}/currentcourses`)
                .then(response => response.json())
                .then(data => {
                    this.registeredCourses = data;
                })
                .catch(error => console.error("Error fetching courses:", error));
        },
        updateProfile() {
            const updatedName = this.newName.trim() || this.name;
            const updatedEmail = this.newEmail.trim() || this.email;

            fetch(`/update_profile`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    userId: this.userId,
                    name: updatedName,
                    email: updatedEmail
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.name = updatedName;
                    this.email = updatedEmail;
                    localStorage.setItem('user', JSON.stringify({ id: this.userId, name: updatedName, email: updatedEmail, role: this.role }));
                    alert("Profile updated successfully!");
                    this.closeEditProfile();
                } else {
                    alert("Error updating profile: " + data.error);
                }
            })
            .catch(error => console.error("Error updating profile:", error));
        },
        openChangePassword() {
            console.log("Opening change password dialog...");
            this.showChangePasswordDialog = true;
        },
        closeChangePassword() {
            this.showChangePasswordDialog = false;
            this.oldPassword = "";
            this.newPassword = "";
            this.confirmNewPassword = "";
        },
        changePassword() {
            // Check if the new passwords match
            if (this.newPassword !== this.confirmNewPassword) {
                alert("New passwords do not match!");
                return;
            }
    
            // Send the old password, new password, and userId to the backend
            fetch(`/change_password`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    userId: this.userId,
                    oldPassword: this.oldPassword,
                    newPassword: this.newPassword
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("Password changed successfully!");
                    this.closeChangePassword();
                } else {
                    alert("Error changing password: " + data.error);
                }
            })
            .catch(error => console.error("Error changing password:", error));
        },
    }
}
