<template>
    <div class="page-search">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Search</h1>
                <h2 class="is-size-5 has-text-grey">Parking zones near: "{{query}}"</h2>
            </div>
        </div>
    </div>
    <div class="columns is-multiline">
      <div
        class = "column is-3"
        v-for="ParkingZone in parking"
        v-bind:key="ParkingZone.id">
        <div class="box">
          <h3 class="is-size-4">{{ParkingZone.name}}</h3>
          <p class="is-size-6 has-text-grey">{{ParkingZone.numSpaces}}</p>
          View details
        </div>
      </div>
    
    </div>
</template>

<script>
    import axios from 'axios'
    export default{
        name: 'LocationSearch',
        data(){
            return{
                locations:[],
                query: '',
                parking: []
            }
        },
        mounted(){
            let uri = window.location.search.substring(1)
            let params = new URLSearchParams(uri)
            
            if(params.get('location')){
                console.log(params.getAll)
                this.query = params.get('location')
                this.performSearch()
            }
            else{
                console.log("I am in the Location Search: the query was blank")
            }
        },
        methods:{
            async performSearch(){
                await axios
                    .post('/api/v1/location/search/', {'query': this.query})
                    .then(response => {
                        this.parking = response.data
                        console.log(response.data)
                    })
                    .catch(error => {
                        console.log(error)
                    })

            }
        }
    }
</script>