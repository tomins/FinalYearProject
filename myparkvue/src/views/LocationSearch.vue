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
                            <button class="button is-dark" @click="setDistance">Submit Filters</button>
                        </div>
                    </div>
                </div>
            </div>
        
        <div class= "columns">
            <div class="column is-12">
                <div class="box  has-background-white-ter">
                    <div class="columns">
                        
                            <div class="column">
                                <h3 class="is-underlined has-text-weight-medium"> Parking Zone Name</h3>
                            </div>
                        
                            <div class="column">
                                <h3 class="is-underlined has-text-weight-medium"> Number of spaces avaliable</h3>
                            </div>
                        
                            <div class="column">
                                <h3 class="is-underlined has-text-weight-medium"> Crimes in the area</h3>
                            </div>
                            <div class="column">
                                <h3 class="is-underlined has-text-weight-medium"> Minimum price</h3>
                            </div>
                        
                            <div class="column">
                                <h3 class="is-underlined has-text-weight-medium"> Distance</h3>
                            </div>
                            <div class="column">
                                <h3 class="is-underlined has-text-weight-medium"> More details</h3>
                            </div>
                    </div>
                </div>
            </div>    
        </div>
        <div class="columns is-multiline">
        <div
            class = "column is-12"
            v-for="ParkingZone in parking"
            v-bind:key="ParkingZone.id">
            <div class="box has-background-grey-lighter	">
                <div class = "columns is-multiline">
                    <div
                        class = "column">
                        <h3 class="is-size-4">{{ParkingZone.name}}</h3>
                    </div>
                    <div
                        class = "column">
                        <p class="is-size-6 has-text-grey">{{ParkingZone.numSpaces}}</p>
                    </div>
                    <div
                        class = "column" :style="{'background-color': isSameColours(ParkingZone.name) }" >
                        <p  class="is-size-6 has-text-black">{{isSame(ParkingZone.name)}}, {{isSameColours(ParkingZone.name)}}</p>
                    </div>
                    <div class = "column">
                        <p class="is-size-6 has-text-grey">{{ParkingZone.rates["price"][0]}}</p>
                    </div>
                    <div class = "column">
                        <p class="is-size-6 has-text-grey">{{ParkingZone.distance.toFixed(2)}} miles</p>
                    </div>
                    
                    <div
                        class = "column">
                        <router-link v-bind:to="ParkingZone.name" class="button is-dark mt-4">View details</router-link>
                    </div>
                </div>
            </div>
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
                parking2: [],
                crime: [],
                distance: 1,
                price: 10,
                max : 0,
                min : 0,
                range : 0,
            }
        },
        
        mounted(){
            //start distance
            var distSlider = document.getElementById("distSlider");
            var distoutput = document.getElementById("distOut");
            distoutput.innerHTML = distSlider.value; 
            distSlider.oninput = function() {
                distoutput.innerHTML = this.value;
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
                await axios
                    .post('/api/v1/location/search/', {
                        'query': this.query,
                        'distance': this.distance
                        })
                    .then(response => {
                        this.parking = response.data
                        console.log(response.data)
                        for (let i = 0; i < this.parking.length; i++) {
                           this.getCrime({ address: this.parking[i].name });
                        }
                        console.log(this.crime)
                        
                    })
                    .catch(error => {
                        console.log(error)
                    })
                
            },
            

            setDistance(){
                var distSlider = document.getElementById("distSlider");
                this.distance = distSlider.value;
                var priceSlider =  document.getElementById("priceSlider");
                this.price = priceSlider.value;
                this.performSearch();
                var i;
                for(i = 0;i<this.parking.length;i++){
                    var rate = this.parking[i].rates["price"][0].replace('£','');
                    if(rate <= this.price){
                        this.parking.splice(indexof(this.parking[i]), 1);
                    }
                }
                console.log("parking2" + this.parking);
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
            isSameColours(name){
                var i;
                this.crimeRating()
                for(i = 0;i<this.crime.length;i++){
                    if(this.crime[i].name === name){
                        return this.crime[i].colour;
                    }
                }
                return "-"
            },
            locDistance(){
                this.distance = 2
            },
            crimeRating(){
                var i;
                
                for(i = 0;i<this.crime.length;i++){
                    if(parseInt(this.crime[i].num_crimes) < this.min){
                        console.log("crimes" + this.crime[i].num_crimes)
                        this.min = this.crime[i].num_crimes
                    }
                    else if(parseInt(this.crime[i].num_crimes) >= this.max){
                        console.log("crimes" + this.crime[i].num_crimes)
                        this.max = this.crime[i].num_crimes;
                    }
                    
                }
                console.log("max" + this.max)
                console.log("min" + this.min)
                this.range = this.max - this.min;
                console.log("range" + this.range)
                var percentage;
                for(i = 0;i<this.crime.length;i++){
                    percentage = this.crime[i].num_crimes/this.range;
                    this.crime[i].percentage = percentage;
                    this.crime[i].colour = this.getColour(percentage);
                }
            },
            getColour(percentage){
                if(percentage <= 0.1){
                    return '#50C878'
                }
                else if(percentage <= 0.2){
                    return '#aaff00'
                }
                else if(percentage <= 0.3){
                    return '#c6e700'
                }
                else if(percentage <= 0.4){
                    return '#dacf00'
                }
                else if(percentage <= 0.5){
                    return '#e9b500'
                }
                else if(percentage <= 0.6){
                    return '#f29b00'
                }
                else if(percentage <= 0.7){
                    return '#f58100'
                }
                else if(percentage <= 0.8){
                    return '#f46611'
                }
                else if(percentage <= 0.9){
                    return '#ee4b2b'
                }
                else{
                    return '#E53935'
                }
                
            }
        }

    }
    
</script>
