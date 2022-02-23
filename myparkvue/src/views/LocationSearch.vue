<template>
    <div class="page-search">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Search</h1>
                <h2 class="is-size-5 has-text-grey">Parking zones near: "{{query}}"</h2>
            </div>
        </div>
        <div class="dropdown is-hoverable">
                <div class="dropdown-trigger">
                    <button class="button" aria-haspopup="true" aria-controls="dropdown-menu">
                        <span>Filters</span>
                        <span class="icon is-small">
                            <i class="fas fa-angle-down" aria-hidden="true"></i>
                        </span>
                    </button>
                </div>
                <div class="dropdown-menu" id="dropdown-menu" role="menu">
                    <div class="dropdown-content">
                        <div class="dropdown-item">
                            <span>Max Distance (miles)</span>
                            <input id="distSlider" class="slider has-output-tooltip is-fullwidth" step="0.2" min="0.2" max="2" value="1" type="range">
                            <span id="distOut">0.2</span>
                        </div>
                        <div class="dropdown-item">
                            <span>Max Price (£)</span>
                            <input id="priceSlider" class="slider has-output-tooltip is-fullwidth" step="0.01" min="0" max="10" value="10" type="range">
                            <span id="priceOut">10</span>
                        </div>
                        <div class="dropdown-item">
                            <span>Crime importance</span>
                            <input id="crimeSlider" class="slider has-output-tooltip is-fullwidth" step="1" min="0" max="10" value="0" type="range">
                            <span id="crimeOut">0</span>
                        </div>
                        <div class="dropdown-item">
                            <button class="button is-dark" @click="performSearch">Submit Filters</button>
                        </div>
                    </div>
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
          <p class="is-size-6 has-text-grey">Number of Crimes in the area: {{isSame(ParkingZone.name)}}</p>
          <router-link v-bind:to="ParkingZone.name" class="button is-dark mt-4">View details</router-link>
        </div>
      </div>
    
    </div>
</template>

<script>
    import axios from 'axios'
    import bulmaSlider from '/node_modules/bulma-extensions/bulma-slider/dist/js/bulma-slider.min.js';
    export default{
        
        name: 'LocationSearch',
        data(){
            return{
                locations:[],
                query: '',
                latlng: '',
                parking: [],
                crime: [],
                distance: 1,
            }
        },
        
        mounted(){
            //start distance
            var distSlider = document.getElementById("distSlider");
            var distoutput = document.getElementById("distOut");
            distoutput.innerHTML = distSlider.value; 
            distSlider.oninput = function() {
                distoutput.innerHTML = this.value;
                this.distance = this.value;
            }
            //end distance, start price
            var priceSlider = document.getElementById("priceSlider");
            var priceOutput = document.getElementById("priceOut");
            priceOutput.innerHTML = priceSlider.value; 
            priceSlider.oninput = function() {
            priceOutput.innerHTML = this.value;
            }
            //end price, start crime
            var crimeSlider = document.getElementById("crimeSlider");
            var crimeOutput = document.getElementById("crimeOut");
            crimeOutput.innerHTML = crimeSlider.value; 
            crimeSlider.oninput = function() {
            crimeOutput.innerHTML = this.value;
            }
            //end crime
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
                console.log(this.distance)
                await axios
                    .post('/api/v1/location/search/', {
                        'query': this.query,
                        'distance': this.distance
                        })
                    .then(response => {
                        this.parking = response.data
                        //for (let i = 0; i < this.parking.length; i++) {
                            //this.getCrime({ address: this.parking[i].name });
                        //}
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
            },
            isSame(name){
                var i;
                for(i = 0;i<this.crime.length;i++){
                    if(this.crime[i].name === name){
                        return this.crime[i].num_crimes;
                    }
                }
                return "-"
            },
            locDistance(){
                this.distance = 2
            }
        }

    }
    
</script>