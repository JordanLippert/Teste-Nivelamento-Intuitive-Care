// app.js
new Vue({
    el: '#app',
    data: {
        searchQuery: '',
        searchResults: []
    },
    methods: {
        search() {
            axios.get('http://localhost:5000/api/search', {
                params: {
                    query: this.searchQuery
                }
            })
            .then(response => {
                this.searchResults = response.data;
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
        }
    }
});