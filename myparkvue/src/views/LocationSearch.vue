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
          <div
            v-for="Crime in crime"
            v-bind:key="Crime.id">
                <div v-if="{{ParkingZone.name}} === {{Crime.name}}">
                    {{Crime.num_crimes}}
                </div>
                
          </div>
          <router-link v-bind:to="ParkingZone.name" class="button is-dark mt-4">View details</router-link>
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
                latlng: '',
                parking: [],
                crime: []
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
                        for (let i = 0; i < this.parking.length; i++) {
                            this.getCrime({ address: this.parking[i].name });
                        }
                        //this.getDistance() this is the start of displaying the parking data by location
                        console.log(response.data)
                    })
                    .catch(error => {
                        console.log(error)
                    })

            },
            getDistance(){//need to add more in here to search correct origin and all destinations(a list of address')
                const service = new google.maps.DistanceMatrixService();
                const r = {
                    origins: ['123 Buckingham Palace Road, London, SW1W 9SR, UK'],
                    destinations: ['Newport Place, London, WC2H 7PU, UK'],
                    travelMode: 'WALKING',
                    }
                service.getDistanceMatrix(r).then((response) => {
                        // put response
                        console.log(response);
                    });
            },

            async getCrime(request){
                const geocoder = new google.maps.Geocoder();
                
                //start get lat long for each parking zone
                await geocoder//needed to add await here as the variable this.latlng wasn't being updatedin time
                    .geocode(request)
                    .then((result)=> {
                        const { results } = result;
                        this.latlng = results[0].geometry.location.toString();
                        
                    })
                    .catch((e) => {
                        console.log("Geocode was not successful for the following reason: " + e);
                    });
                //end get latlng for each parking zone
                await axios//this is going to give django the parameters to search the DB/Api for crime by, it will return the crime data
                    .post('/api/v1/crime/search/', {
                        'name': request,
                        'latlng': this.latlng,
                        })
                    .then(response => {
                        this.crime.push(response.data)
                        console.log(this.crime)
                    })
                    .catch(error => {
                        console.log(error)
                    })
            }
        }

    }
</script>