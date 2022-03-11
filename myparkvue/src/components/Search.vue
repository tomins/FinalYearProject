
<template>

    <form method="get" action="/LocationSearch">
        <div class="field has-addons">
            <div class="control has-icons-left">
                <input name="location" type="text" class="input is-large" placeholder="Search Address" ref="location">
                <span class="icon is-left">
                    <i class="fas fa-search"></i>
                </span>
            </div>
            <div class="control">
            <button class="button is-primary is-large">Search</button><!--@click="sendLocation" -->
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
            console.log(autocomplete.getPlace());
            axios
                .post('/api/v1/location/create/', {
                    'name': autocomplete.getPlace().name,
                    'address' : autocomplete.getPlace().adr_address,
                    'lat' : autocomplete.getPlace().geometry.viewport.Sa.h,
                    'long' : autocomplete.getPlace().geometry.viewport.wb.h,
                    })
                .then(response => {
                    console.log(response.data);
                })
                .catch(error => {
                    console.log(error)
                })
        })
    }
}
</script>
