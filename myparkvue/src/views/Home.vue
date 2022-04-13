<template>
  <div class="home">
    <section class="hero is-medium is-dark mb-6">
      <div class = "hero-body has-text-centered">
        <p class = "title mb-6">
          Welcome to my park
        </p>
        <p class="subtitle">
          The best parking app on the web!
        </p>
      </div>
    </section>
    <div class="columns is-centered is-mobile">
      <div class="column is-half is-offset-2">
       <Search> </Search>
       </div>
    </div>
    <div v-if="!$store.state.token == ''" class="columns is-centered is-mobile">
      <div class="column is-half is-offset-4">
        <div class="dropdown is-hoverable">
          <div class="dropdown-trigger">
            <button class="button" aria-haspopup="true" aria-controls="dropdown-menu">
              <span>Your Favorite Locations</span>
              <span class="icon is-small">
                <i class="fas fa-angle-down" aria-hidden="true"></i>
              </span>
            </button>
          </div>
          <div class="dropdown-menu" id="dropdown-menu" role="menu">
            <div class="dropdown-content"
              v-for="Favoritelocation in favoriteLocations"
              v-bind:key="Favoritelocation.id">
                <div class="dropdown-item">
                  <router-link ref="location" v-bind:to="`/LocationSearch?location=`+ Favoritelocation.location.name + ', ' + Favoritelocation.location.address">{{Favoritelocation.location.name}}</router-link>
                </div>
            </div>
          </div>
        </div>
      </div>
    </div>    
  </div>
</template>

<script>
import Search from '@/components/Search.vue'
import axios from 'axios'
export default {
  name: 'Home',
  data(){
    return {
      favoriteLocations: [],
    }
  },
  components: { 
    Search
  },
  mounted(){
    document.title = 'Home | MyPark'
    this.getFavorites();
  },
  methods:{
    async getFavorites(){
      await axios
        .get('api/v1/get-favorite/',{
          })
          .then(response => {
          this.favoriteLocations = response.data
          console.log(response.data)
          })
          .catch(error => {
          console.log(error)
          })
    }
  },
}
</script>

<style scoped>
  .image{
    margin-top: -1.15rem;
    margin-left: -1.15rem;
    margin-right: -1.15rem;
  }
</style>
