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
      <div class="column is-half is-offset-3">
       <Search> </Search>
       </div>
    </div>
    
    
     
   



    <!-- <div class="columns is-multiline">
      <div class="column is-12">
        <h2 class="is-size-2 has-text-centered"> Latest Products</h2>
      </div>
      <div
        class = "column is-3"
        v-for="product in latestProducts"
        v-bind:key="product.id">
        <div class="box">
          <figure class="image mb-4">
            <img bind:src="product.get_thumbnail">
          </figure>
          <h3 class="is-size-4">{{product.name}}</h3>
          <p class="is-size-6 has-text-grey">€{{product.price}}</p>
          View details
        </div>
      </div>
    
    </div>
      -->
  </div>
</template>

<script>
import Search from '@/components/Search.vue'
export default {
  name: 'Home',
  data(){
    return {

    }
  },
  components: { 
    Search
  },
  mounted(){
    document.title = 'Home | MyPark'
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
