<template>
    <div class="page-search">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Search</h1>
                <h2 class="is-size-5 has-text-grey">Search term: "{{query}}"</h2>
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
                query: ''
            }
        },
        mounted(){
            let uri = window.location.search.substring(1)
            let params = new URLSearchParams(uri)
            
            if(params.get('location')){
                
                this.query = params.get('location')
                this.performSearch()
            }
            else{
                console.log("I am in the Location Search: the quey was blank")
            }
        },
        methods:{
            async performSearch(){
                await axios
                    .post('/api/v1/location/search/', {'query': this.query})
                    .then(response => {
                        this.locations = response.data
                    })
                    .catch(error => {
                        console.log(error)
                    })

            }
        }
    }
</script>