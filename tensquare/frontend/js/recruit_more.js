var vm = new Vue({
    el: "#app",
    data: {
        latestJobList: [],
        hotEnterpriseList: [],
        cityList: [],
        searchCity: '北京',
        keyword: ''
    },
    mounted() {
        var params = get_query_string('name');
        if (params) {
            this.searchCity = params;
        }

        this.getHotCity();
        this.searchJob();
        this.getHotEnterpriseList();
    },
    methods: {
        getHotCity() {
            var url = host + 'city/hotlist/';
            axios.get(url).then(response => {
                this.cityList = response.data;
            }).catch(error => { });
        },
        searchJob() {
            var url = host + 'recruits/search/city/keyword/'
            axios.post(url, {
                cityname: this.searchCity,
                keyword: this.keyword
            }).then(response => {
                console.log(response.data)
                this.latestJobList = response.data;
            }).catch(error => { });
        },
        getHotEnterpriseList() {
            var url = host + 'enterprise/search/hotlist/'
            axios.get(url).then(response => {
                this.hotEnterpriseList = response.data;
            }).catch(error => { });
        }
    },

});