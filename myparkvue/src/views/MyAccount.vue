<template>
    <div class="page-my-account">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">My Account</h1>
            </div>
            <div class="column is-12">
                <button @click="logout()" class="button is-danger">Log out</button>
                <div
                    class = "column is-12"
                    v-for="loc in favoriteLocations"
                    v-bind:key="loc.id">
                    <div class="box has-background-grey-lighter	">
                        <div class = "columns is-multiline">
                            <div class = "column">
                                <h3 class="is-size-4">{{loc.location.name}}</h3>
                            </div>
                            <div class = "column">
                                <button class="button is-fullwidth is-danger" v-on:click="this.removeFavoriteLocation(loc.location.name)">
                                    <span class="icon is-left">
                                        Remove from Favorites<i class="fa-solid fa-delete-left" />
                                    </span>
                                </button>
                            </div>
                            
                        </div>
                    </div>
                </div>
            </div>
            
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default{
    name: 'MyAccount',
    data() {
        return {
            favoriteLocations: [],
        }
    },
    mounted(){
        document.title = 'MyAccount | MyPark'
        this.getFavorites()
    },
    methods:{
        logout(){
            axios.defaults.headers.common['Authorization'] = ""
            localStorage.removeItem("token")
            localStorage.removeItem("username")
            localStorage.removeItem("password")

            this.$store.commit('removeToken')

            this.$router.push('/')
        },
        async getFavorites() {
            await axios
                .get('api/v1/get-favorite/', {
                })
                .then(response => {
                this.favoriteLocations = response.data
                })
                .catch(error => {
                console.log(error)
                })
        },
        async removeFavoriteLocation(query){
            console.log(query)
            await axios
                .put('api/v1/favoritelocation/delete/',{
                    'query': query,
                })
                .then(response => {
                console.log(response)
                getFavorites()
                })
                .catch(error => {
                console.log(error)
                })
        }
    },

    
}
</script>
