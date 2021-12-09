<template>
    <div class="field has-addons">
        <div class="control has-icons-left">
            <input type="text" class="input is-large" placeholder="Search Address" ref="location">
            <span class="icon is-left">
                <i class="fas fa-search"></i>
            </span>
        </div>
        <div class="control">
        <button class="button is-primary is-large">Search</button>
        </div>
    </div>
</template>

<script>
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
        })
    }
}
</script>
