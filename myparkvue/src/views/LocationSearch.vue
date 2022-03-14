<template>
    <div class="page-search">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Search</h1>
                <h2 class="is-size-5 has-text-grey">Parking zones near: "{{this.query}}"</h2>
            </div>
        </div>
        <nav class="level">
            <div class="level-left">
                <div class="level-item">
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
                                        <input id="crimeSlider" class="slider has-output-tooltip is-fullwidth" step="1" min="0" max="10" value="10" type="range">
                                        <span id="crimeOut">10</span>
                                    </div>
                                    <div class="dropdown-item">
                                        <button class="button is-dark" @click="setDistance">Submit Filters</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                    <div class="level-right">
                        <div class="level-item">
                            <button class="button is-dark" v-on:click="listView = !listView">ToggleMap View</button>
                        </div>
                    </div>
                </nav>
            
        <transition name="fade">
            <div v-show="listView">
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
                                    <div class="column">
                                        <h3 class="is-underlined has-text-weight-medium"> Overall rating</h3>
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
                                class = "column has-text-justified" :style="{'background-color': getSpacesColour(ParkingZone.name) }">
                                <p class="is-size-6 has-text-black">{{ParkingZone.numSpaces}}</p>
                            </div>
                            <div
                                class = "column has-text-justified" :style="{'background-color': isSameColours(ParkingZone.name) }" >
                                <p  class="is-size-6 has-text-black">{{isSame(ParkingZone.name)}}</p>
                            </div>
                            <div class = "column has-text-justified" :style="{'background-color': getPriceColour(ParkingZone.name) }">
                                <p class="is-size-6 has-text-black">{{ParkingZone.rates["price"][0]}}</p>
                            </div>
                            <div class = "column" :style="{'background-color': getDistanceColour(ParkingZone.name) }">
                                <p class="is-size-6 has-text-black">{{ParkingZone.distance.toFixed(2)}} miles</p>
                            </div>
                            
                            <div
                                class = "column">
                                <router-link v-bind:to="ParkingZone.name" class="button is-dark mt-4">View details</router-link>
                            </div>
                            <div class = "column"  :style="{'background-color': getOverallColour(ParkingZone.name) }">
                                <p class="is-size-6 has-text-black">{{ParkingZone.overallRate.toFixed(2)}} </p>
                            </div>
                        </div>
                    </div>
                </div>
                
            </div>
        </div>
    
    </transition>
    <transition name="fade">
        <div v-show="!listView">
            <div id="map2" ref="maps" style="width:700px; height:500px; margin-left:80px;">
                This is a map
            </div>
        </div>
    </transition>
    
    
    </div>
</template>

<script>
    import axios from 'axios'
    //import { Loader } from "@googlemaps/js-api-loader"
    //import bulmaSlider from '/node_modules/bulma-extensions/bulma-slider/dist/js/bulma-slider.min.js';
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
                locationLatLong: [],
                distance: 1,
                price: 10,
                crimeFilter: 10,
                crimeMax : 0,
                crimeMin : 1000,
                crimeRange : 0,
                spacesRange: 0,
                spacesMax: 0,
                spacesMin: 1000,
                priceMax: 0,
                priceMin: 1000,
                priceRange: 0,
                distanceMin: 10000,
                distanceMax: 0,
                distanceRange: 0,
                overallMax: 0,
                overallMin: 100,
                overallRange: 100,
                listView: true,
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
                this.query = params.get('location')
                this.performSearch()
            }
            else{
                console.log("I am in the Location Search: the query was blank")
            }  

            
        },
        
        methods:{

            
            async setMarkers(){//called from perform search so everything is loaded first
                await axios
                    .post('api/v1/location/getDetails',{
                        'query':this.query
                    })
                    .then(response => {
                        this.locationLatLong = response.data
                        console.log(response.data)
                    })
                    .catch(error => {
                        console.log(error)
                    })
                //create actual map
                const map = new google.maps.Map(document.getElementById('map2'), {
                    center: { lat: parseFloat(this.locationLatLong[0].long), lng: parseFloat(this.locationLatLong[0].lat) },
                    zoom: 12
                });
                //end create map
                
                //location marker
                const Locmarker = new google.maps.Marker({
                    position: { lat: parseFloat(this.locationLatLong[0].long), lng: parseFloat(this.locationLatLong[0].lat) },
                    map: map,
                    title: this.locationLatLong[0].name
                });
                //end location marker

                //start parkingZone markers
                for (let i = 0; i < this.parking.length; i++) {
                    var a = this.parking[i].latlong
                    const b = a.split(",");
                    var parkLat = b[0];
                    var parkLong = b[1];
                    parkLat = parkLat.split(":")[1]
                    parkLong = parkLong.split(":")[1]
                    const marker = new google.maps.Marker({
                        position: { lat: parseFloat(parkLat), lng: parseFloat(parkLong) },
                        map: map,
                        icon: "https://developers.google.com/maps/documentation/javascript/examples/full/images/parking_lot_maps.png",
                        title: this.parking[i].name
                    });
                }
                //end parkingZone marker
            },
            async performSearch(){
                
                await axios
                    .post('/api/v1/location/search/', {
                        'query': this.query,
                        'distance': this.distance
                        })
                    .then(response => {
                        this.parking = response.data
                        for (let i = 0; i < this.parking.length; i++) {
                           this.getCrime({ address: this.parking[i].name });
                        }
                        this.setMarkers();
                        
                    })
                    .catch(error => {
                        console.log(error)
                    })
                
                
            },
            

            setDistance(){
                var distSlider = document.getElementById("distSlider");
                
                var priceSlider =  document.getElementById("priceSlider");
                var crimeSlider = document.getElementById("crimeSlider");
                if(this.distance != distSlider.value){
                    this.distance = distSlider.value;
                    this.performSearch();
                }
                if(this.price != priceSlider.value){
                    this.price = priceSlider.value;
                    var i;
                    for(i = 0;i<this.parking.length;i++){
                        if(parseFloat(this.parking[i].rates["price"][0].replace('£','')) > this.price){
                            this.parking.splice(i, 1);
                        }
                    }
                }
                if(this.crimeFilter != crimeSlider.value){
                    this.crimeFilter = crimeSlider.value;
                    var i;
                    for(i = 0;i<this.crime.length;i++){
                        if(this.crime[i].percentage > (this.crime/10)){
                            for(x = 0;x<this.parking.length;x++){
                                if(this.parking[x].name === this.crime[i].name){
                                    this.parking.splice(x, 1);
                                }
                            }
                        }
                    }
                }
                
            },
            combinedRating(){
                var i;
                var x;
                var distancePer;
                var spacesPer;
                var pricePer;
                var crimePer;
                 

                for(i = 0;i<this.parking.length;i++){
                    spacesPer = this.parking[i].percentage;
                    distancePer = this.parking[i].distancePercentage;
                    pricePer = this.parking[i].pricePercentage;
                    for(x = 0;x<this.crime.length;x++){
                        if(this.crime[x].name === this.parking[i].name){
                            crimePer = this.crime[x].percentage;
                        }
                    }
                    this.parking[i].overallRate = (spacesPer + pricePer + crimePer + distancePer)/4;
                    if(this.parking[i].overallRate > this.overallMax){
                        this.overallMax = this.parking[i].overallRate;
                    }
                    else if(this.parking[i].overallRate < this.overallMin){
                        
                        this.overallMin = this.parking[i].overallRate;
                    }
                }
                this.overallRange = this.overallMax - this.overallMin;
                var percentage;
                var minus;
                
                for(i = 0;i<this.parking.length;i++){
                    minus = this.parking[i].overallRate - this.overallMin;
                    percentage = minus/this.overallRange;
                    this.parking[i].overallPer = percentage;
                    this.parking[i].overallColor = this.getColour(percentage);
                }
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
                this.combinedRating()
                this.sortByRating()
                for(i = 0;i<this.crime.length;i++){
                    if(this.crime[i].name === name){
                        return this.crime[i].colour;
                    }
                }
                return "-"
            },
            getSpacesColour(name){
                var i;
                this.spacesRating()
                for(i = 0;i<this.parking.length;i++){
                    if(this.parking[i].name === name){
                        return this.parking[i].colour;
                    }
                } 
            },
            getOverallColour(name){
                var i;
                for(i = 0;i<this.parking.length;i++){
                    if(this.parking[i].name === name){
                        return this.parking[i].overallColor;
                    }
                } 
            },
            getDistanceColour(name){
                var i;
                this.distanceRating();
                for(i = 0;i<this.parking.length;i++){
                    if(this.parking[i].name === name){
                        return this.parking[i].distanceColour;
                    }
                } 
            },
            getPriceColour(name){
                var i;
                this.priceRating();
                for(i = 0;i<this.parking.length;i++){
                    if(this.parking[i].name === name){
                        return this.parking[i].priceColour;
                    }
                }
            },
            locDistance(){
                this.distance = 2
            },
            spacesRating(){
                 var i;
                
                for(i = 0;i<this.parking.length;i++){
                    if(parseInt(this.parking[i].numSpaces) > this.spacesMax){
                        this.spacesMax = this.parking[i].numSpaces;
                    }
                    else if(parseInt(this.parking[i].numSpaces) < this.spacesMin){
                        this.spacesMin = this.parking[i].numSpaces;
                    }
                    
                }
                this.spacesRange = this.spacesMax - this.spacesMin;
                var percentage;
                var minus;
                for(i = 0;i<this.parking.length;i++){
                    minus = this.parking[i].numSpaces - this.spacesMin;
                    percentage = minus/this.spacesRange;
                    this.parking[i].percentage = percentage;
                    this.parking[i].colour = this.getColour(percentage);
                }
            },
            priceRating(){
                var i;
                
                for(i = 0;i<this.parking.length;i++){
                    var priceWithout = this.parking[i].rates["price"][0].replace(/£/g,'');
                   if(priceWithout > this.priceMax){
                       this.priceMax = priceWithout;
                   }
                   else if(priceWithout< this.priceMin){
                       this.priceMin = priceWithout;
                   }
                }
                this.priceRange = this.priceMax - this.priceMin;
                var percentage;
                var minus;
                for(i = 0;i<this.parking.length;i++){
                    var priceWithout = this.parking[i].rates["price"][0].replace(/£/g,'');
                    minus = priceWithout - this.priceMin
                    percentage = minus/this.priceRange;
                    this.parking[i].pricePercentage = percentage;
                    this.parking[i].priceColour = this.getColour(percentage);
                }
            },
            crimeRating(){
                var i;
                
                for(i = 0;i<this.crime.length;i++){
                    if(parseInt(this.crime[i].num_crimes) > this.crimeMax){
                        this.crimeMax = this.crime[i].num_crimes
                    }
                    else if(parseInt(this.crime[i].num_crimes) < this.crimeMin){
                        this.crimeMin = this.crime[i].num_crimes;
                    }
                    
                }
                this.crimeRange = this.crimeMax - this.crimeMin;
                var percentage;
                var minus;
                for(i = 0;i<this.crime.length;i++){
                    minus = this.crime[i].num_crimes - this.crimeMin;
                    percentage = minus/this.crimeRange;
                    this.crime[i].percentage = percentage;
                    this.crime[i].colour = this.getColour(percentage);
                }
            },
            distanceRating(){
                var i;
                
                for(i = 0;i<this.parking.length;i++){
                    if(parseFloat(this.parking[i].distance) > this.distanceMax){
                        this.distanceMax = parseFloat(this.parking[i].distance);
                    }
                    else if(parseFloat(this.parking[i].distance) < this.distanceMin){
                        
                        this.distanceMin = parseFloat(this.parking[i].distance);
                    }
                    
                }
                this.distanceRange = this.distanceMax - this.distanceMin;
                var percentage;
                var minus;
                for(i = 0;i<this.parking.length;i++){
                    minus = this.parking[i].distance - this.distanceMin;
                    percentage = minus/this.distanceRange;
                    this.parking[i].distancePercentage = percentage;
                    this.parking[i].distanceColour = this.getColour(percentage);
                }
            },
            sortByRating(){
                console.log(this.parking[2].overallPer)
                this.parking.sort(function(a, b){return a.overallPer - b.overallPer});
                console.log(this.parking[2].overallPer)
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
