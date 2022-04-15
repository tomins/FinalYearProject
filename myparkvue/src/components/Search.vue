
<template>

    <form method="get" action="/LocationSearch">
        <div class="field has-addons">
            <div class="control has-icons-left">
                <input name="location" type="text" class="input is-large" placeholder="Search Address" ref="location" :style="{'background-color': '#bdfff6', 'color': '#e23c52' }">
                <span class="icon is-left">
                    <i class="fas fa-search"></i>
                </span>
            </div>
            <div class="control">
            <button class="button is-large" :style="{'background-color': '#bdfff6', 'color': '#e23c52' }">Search</button>
            </div>
        </div>
    </form>
    
    
    
</template>

<script>
import axios from 'axios'
export default {
    name: 'Search',
    mounted(){
        const autocomplete = new google.maps.places.Autocomplete(
            this.$refs["location"],
            {
                bounds: new google.maps.LatLngBounds(
                    new google.maps.LatLng(51.5014, 0.1419)
                )
            }
        );
        
        autocomplete.addListener("place_changed", () => {
            console.log(autocomplete.getPlace().geometry.location.lat());
            axios
                .post('/api/v1/location/create/', {
                    'name': autocomplete.getPlace().name,
                    'address' : autocomplete.getPlace().adr_address,
                    'lat' : autocomplete.getPlace().geometry.location.lat(),
                    'long' : autocomplete.getPlace().geometry.location.lng(),
                    })
                .then(response => {
                    console.log(response);
                })
                .catch(error => {
                    console.log(error)
                })
        })
    },
}
</script>
