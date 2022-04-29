<template>
  <div class="home">
    <section class="hero is-medium mb-6" :style="{'background-color': '#000000' }">
      <div class = "hero-body has-text-centered">
        <p class = "title mb-6" :style="{'color': '#ffffff' }">
          Welcome to my park
        </p>
        <p class="subtitle" :style="{'color': '#ffffff' }">
          The best parking app on the web!
        </p>
        <p class="subtitle" :style="{'color': '#ffffff' }">
          Simply type in where you want to go and we will find you the best parking space possible!
        </p>
        <p class="subtitle" :style="{'color': '#ffffff' }">
          If you would like to get even more features then log in to you're account or create one if you haven't already, its free!
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
            <button class="button" aria-haspopup="true" aria-controls="dropdown-menu"  :style="{'background-color': '#000000', 'color': '#ffffff' }">
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
