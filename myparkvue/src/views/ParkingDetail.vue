<template>
    <div class="page-parking">
        <div class="columns is-multiline">
            <div class = "column is-6"
                v-for="ParkingZone in parking"
                v-bind:key="ParkingZone.id">
                
                <div class="tile is-parent is-vertical is-primary box " :style="{'background-color': '#000000', 'color': '#ffffff' }">
                    <h3 class="is-size-2 is-underlined">{{ParkingZone.name}}</h3>
                </div>
                <div class="tile is-child is-vertical box" :style="{'background-color': '#000000', 'color': '#ffffff' }">
                    <a class="button" :style="{'background-color': '#ffffff', 'color': '#000000' }" v-bind:href="bookingLink(ParkingZone.name)"> Booking</a>
                </div>
                <div class="tile is-child is-vertical notification box" :style="{'background-color': '#000000', 'color': '#ffffff' }">
                <span class="subtitle is-size-3 is-underlined">
                    Details
                </span>
                <div class="tile is-child is-vertical box" :style="{'background-color': '#000000', 'color': '#ffffff' }">
                    <p class="is-size-5 "> Address:   {{ParkingZone.address}}</p>
                </div>
                <div class="tile is-child is-vertical box" :style="{'background-color': '#000000', 'color': '#ffffff' }">
                    <p class="is-size-5"> Number of spaces:   {{ParkingZone.numSpaces}}</p>
                </div>
                <div class="tile is-child is-vertical box" :style="{'background-color': '#000000', 'color': '#ffffff' }">
                    <p class="is-size-5"> Number of disabled bays:   {{ParkingZone.disabledBays}}</p>
                </div>
                <div class="tile is-child is-vertical box" :style="{'background-color': '#000000', 'color': '#ffffff' }">
                    <p class="is-size-5 "> Number of electric charging bays:   {{ParkingZone.evSpaces}}</p>
                </div>
                <div class="tile is-child is-vertical box" :style="{'background-color': '#000000', 'color': '#ffffff' }">
                    <p class="is-size-5"> Max height of entry:   {{ParkingZone.height}}m</p>
                </div>
                <div class="tile is-child is-vertical box" :style="{'background-color': '#000000', 'color': '#ffffff' }">
                    <div class = "column is-6"
                        v-for="service in ParkingZone.services.list"
                        v-bind:key="service.list">
                        <p class="is-size-5 has-text-weight-semibold">List of Services Avaliable:</p>
                        <div class = "column is-6"
                            v-for="serve in service"
                            v-bind:key="serve.list">
                        <p class="is-size-5">{{serve}}</p>
                        </div>
                    </div>
                </div>
                <div class="tile is-child is-vertical box" :style="{'background-color': '#000000', 'color': '#ffffff' }">
                    <div class = "column is-6"
                        v-for="security in ParkingZone.security.list"
                        v-bind:key="security.list">
                        <p class="is-size-5 has-text-weight-semibold">List of Security Avaliable:</p>
                        <div class = "column is-6"
                            v-for="serve in security"
                            v-bind:key="serve.list">
                        <p class="is-size-5">{{serve}}</p>
                        </div>
                    </div>
                </div>
                <div class="tile is-child is-vertical box" :style="{'background-color': '#000000', 'color': '#ffffff' }">
                    <p class="is-size-5 has-text-weight-semibold">Opening Hours:</p>
                    <div class = "column is-6"
                        v-for="openingDays,openingHours   in ParkingZone.openingHours"
                        v-bind:key="openingHours">
                        <p class="is-size-5 has-text-weight-medium is-capitalized">{{openingHours}}:</p>
                        <p class="is-size-5">{{openingDays}}</p>
                        
                    </div>
                </div>
                <div class="tile is-child is-vertical box" :style="{'background-color': '#000000', 'color': '#ffffff' }">
                    <table class="table" :style="{'background-color': '#000000', 'color': '#ffffff' }">
                        <thead>
                            <tr>
                                <th><abbr title="Rates" :style="{'background-color': '#000000', 'color': '#ffffff' }">Rates</abbr></th>   
                            </tr>
                        </thead>
                    </table>
                    <div class = "column is-6"
                        v-for="openingDays,openingHours   in ParkingZone.rates"
                        v-bind:key="openingHours" >
                        <div class="tile is-child box" :style="{'background-color': '#000000', 'color': '#ffffff' }">
                        <p class="is-size-5 has-text-weight-medium is-capitalized">{{openingHours}}:</p>
                        </div>
                        <div class="tile is-child box" :style="{'background-color': '#000000', 'color': '#ffffff' }">
                        <p class="is-size-5">{{openingDays[0]}}</p>
                        </div>
                        
                    </div>
                </div>
                </div>
          
        
      
                
            </div>
            <div class="column is-6" >
                
                <h2 class="subtitle" :style="{'color': '#ffffff' }">Map View</h2>

                <div id="map2" ref="maps" style="width:100%; height:700px;">
                Map Loading....
                </div>
            </div>

            
        </div>
        
    </div> 
</template>

<script>
import axios from 'axios'
export default{
    name: 'ParkingDetail',
    data(){
        return{
            parking:{}
        }
    },
    mounted(){
        document.title = 'Parking Detail | MyPark'
        this.getParkingDetail()
       
    },
    methods:{
        async getParkingDetail(){
            const name = this.$route.params.name

            await axios
                .post('/api/v1/ParkingZone/ParkingDetail/', {'query': name})
                .then(response => {
                    this.parking  = response.data
                    this.createMap()
                })
                .catch(error => {
                    console.log(error)
                })
        },
        createMap(){
            
            var a = this.parking[0].latlong
            const b = a.split(",");
            var parkLat = b[0];
            var parkLong = b[1];
            parkLat = parkLat.split(":")[1]
            parkLong = parkLong.split(":")[1]
            const map = new google.maps.Map(document.getElementById('map2'), {
                center: { lat: parseFloat(parkLat), lng: parseFloat(parkLong) },
                zoom: 14
            });
            const marker = new google.maps.Marker({
                position: { lat: parseFloat(parkLat), lng: parseFloat(parkLong) },
                map: map,
                icon: "https://developers.google.com/maps/documentation/javascript/examples/full/images/parking_lot_maps.png",
                title: this.parking[0].name
                });
        },

        bookingLink(name){
            console.log("name" + name)
            const nm = name.split("Q-Park")
            console.log(nm[1])
            let n = nm[1].replace(" ", "-")
            console.log(n)

            return "https://www.q-park.co.uk/en-gb/cities/london/" + n
        }
    }
}
</script>