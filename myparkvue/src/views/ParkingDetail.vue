<template>
    <div class="page-parking">
        <div class="columns is-multiline">
            <div class = "column is-6"
                v-for="ParkingZone in parking"
                v-bind:key="ParkingZone.id">
                
                <div class="tile is-parent is-vertical is-primary box ">
                <h3 class="is-size-2 is-underlined">{{ParkingZone.name}}</h3>
                </div>
                <div class="tile is-child is-vertical notification box">
                <span class="subtitle is-size-3">
                    Details
                </span>
                <div class="tile is-child is-vertical box">
                    <p class="is-size-5 has-text-grey"> Address:   {{ParkingZone.address}}</p>
                </div>
                <div class="tile is-child is-vertical box">
                    <p class="is-size-5 has-text-grey"> Number of spaces:   {{ParkingZone.numSpaces}}</p>
                </div>
                <div class="tile is-child is-vertical box">
                    <p class="is-size-5 has-text-grey"> Number of disabled bays:   {{ParkingZone.disabledBays}}</p>
                </div>
                <div class="tile is-child is-vertical box">
                    <p class="is-size-5 has-text-grey"> Number of electric charging bays:   {{ParkingZone.evSpaces}}</p>
                </div>
                <div class="tile is-child is-vertical box">
                    <p class="is-size-5 has-text-grey"> Max height of entry:   {{ParkingZone.height}}m</p>
                </div>
                <div class="tile is-child is-vertical box">
                    <div class = "column is-6"
                        v-for="service in ParkingZone.services.list"
                        v-bind:key="service.list">
                        <p class="is-size-5 has-text-weight-semibold">List of Services Avaliable:</p>
                        <div class = "column is-6"
                            v-for="serve in service"
                            v-bind:key="serve.list">
                        <p class="is-size-5 has-text-grey">{{serve}}</p>
                        </div>
                    </div>
                </div>
                <div class="tile is-child is-vertical box">
                    <div class = "column is-6"
                        v-for="security in ParkingZone.security.list"
                        v-bind:key="security.list">
                        <p class="is-size-5 has-text-weight-semibold">List of Security Avaliable:</p>
                        <div class = "column is-6"
                            v-for="serve in security"
                            v-bind:key="serve.list">
                        <p class="is-size-5 has-text-grey">{{serve}}</p>
                        </div>
                    </div>
                </div>
                <div class="tile is-child is-vertical box">
                    <p class="is-size-5 has-text-weight-semibold">Opening Hours:</p>
                    <div class = "column is-6"
                        v-for="openingDays,openingHours   in ParkingZone.openingHours"
                        v-bind:key="openingHours">
                        <p class="is-size-5 has-text-weight-medium is-capitalized">{{openingHours}}:</p>
                        <p class="is-size-5 has-text-grey">{{openingDays}}</p>
                        
                    </div>
                </div>
                <div class="tile is-child is-vertical box">
                    <table class="table">
                        <thead>
                            <tr>
                                <th><abbr title="Rates">Rates</abbr></th>   
                            </tr>
                        </thead>
                    </table>
                    <div class = "column is-6"
                        v-for="openingDays,openingHours   in ParkingZone.rates"
                        v-bind:key="openingHours">
                        <div class="tile is-child box">
                        <p class="is-size-5 has-text-weight-medium is-capitalized">{{openingHours}}:</p>
                        </div>
                        <div class="tile is-child box">
                        <p class="is-size-5 has-text-grey">{{openingDays}}</p>
                        </div>
                        
                    </div>
                </div>
                </div>
          
        
      
                
            </div>
            <div class="column is-6">

                <h2 class="subtitle">Map View</h2>

                <p>Map Goes Here</p>
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
        this.getParkingDetail()
    },
    methods:{
        async getParkingDetail(){
            const name = this.$route.params.name
            console.log(name)

            await axios
                .post('/api/v1/ParkingZone/ParkingDetail/', {'query': name})
                .then(response => {
                    this.parking  = response.data
                    console.log(response.data)
                })
                .catch(error => {
                    console.log(error)
                })
        }
    }
}
</script>