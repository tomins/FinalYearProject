<template>
  <div id="wrapper" :style="{'background-color': '#888c8d' }">
    <nav class="navbar" :style="{'background-color': '#000000' }">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item"><strong :style="{'color': '#ffffff' }">My Park</strong></router-link>
        <a class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbar-menu" @click="showMobileMenu = !showMobileMenu">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>
      <div class="navbar-menu" id="navbar-menu" v-bind:class="{'is-active': showMobileMenu}">
        <div class="navbar-end">
          
          <div class="navbar-item">
            <div class="buttons">
              <template v-if="!$store.state.token == ''" >
                <router-link to="/my-account" class="button" :style="{'background-color': '#888c8d' }"><strong :style="{'color': '#000000' }">My Account</strong></router-link>
              </template>
              <template v-else>
                <router-link to="/log-in" class="button" :style="{'background-color': '#888c8d', 'color' : '#000000' }"><strong>Login</strong></router-link>
              </template>
              
            </div>
          </div>
        </div>
      </div>
    </nav>
    <section class="section">
      <router-view/>
    </section>
    
    <footer class="footer" :style="{'background-color': '#000000' }">
      <template v-if="!$store.state.token == ''" >
        <p class="has-text-centered" :style="{'color': '#ffffff' }">Thanks for logging in!</p>
      </template>
      <template v-else>
        <p class="has-text-centered" :style="{'color': '#ffffff' }">Log in for more!</p>
      </template>
      
    </footer>
  </div>
</template>

<script>
import axios from 'axios'

export default{
  data() {
    return{
      showMobileMenu: false,//to show a menu on show a menu
    }
  },
  beforeCreate(){
    this.$store.commit('initializeStore') 
    const token = this.$store.state.token
    if(!token == ''){
      axios.defaults.headers.common['Authorization']="Token " + token
    }else{
      axios.defaults.headers.common['Authorization']=""
    }
  }
}
</script>


<style lang="scss">
  @import '../node_modules/bulma';
</style>
