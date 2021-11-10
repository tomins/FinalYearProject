<template>
    <div class="page sign-in">
        <div class="column is-4 is-offset-4">
            <h1 class="title">Log In</h1>
            <form @submit.prevent="submitForm">
                <div class="field">
                    <label>Username</label>
                    <div class="control">
                        <input type="text" class="input" v-model="username">
                    </div>
                </div>
                <div class="field">
                    <label>Password</label>
                    <div class="control">
                        <input type="password" class="input" v-model="password">
                    </div>
                </div>
                <div class="notification is-danger" v-if="errors.length">
                    <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                </div>
                <div class="field">
                    <div class="control">
                        <button class="button is-dark">Sign Up</button>
                    </div>
                </div>
                <hr>

                OR <router-link to="/sign-up">click here</router-link> to sign up!
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default{
    name: 'LogIn',
    data(){
        return{
            username: '',
            password: '',
            errors: []
        }
    },
    mounted(){
        document.title = 'Log In | MyPark'
    },
    methods:{
        async submitForm(){
            axios.defaults.headers.common['Authorization'] = ""
            localStorage.removeItem("token")

            const formData= {
                username: this.username,
                password: this.password
            }
            await axios
                .post("/api/v1/token/login/",formData)
                .then(response=> {
                    const token = response.data.auth.token
                    this.$store.commit('setToken', token)
                    axios.defults.headers.common['Authorization'] = "Token " + token
                    localStorage.setItem("token", token)
                    const toPath = this.$route.query.to || '/'
                    this.$router.push(toPath)
                })
                .catch(error =>{
                    if(error.response){
                        for(const property in error.response.data){
                            this.errors.push(`${property}: ${error.response.data[property]}`)
                        }
                    }else{
                        this.errors.push('Something went wrong!')
                        console.log(JSON.stringify(error))
                    }
                })
        }
    }
}
</script>



