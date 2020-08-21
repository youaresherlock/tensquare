var vm = new Vue({
    el: "#app",
    data: {
        recommendJobList: [],
        latestJobList: [],
        hotEnterpriseList: []
    },
    mounted() {
        this.getRecommendJobList();
        this.getLatestJobList();
        this.getHotEnterpriseList();
    },
    methods: {
        getRecommendJobList() {
            var url = host + 'recruits/search/recommend/'
            axios.get(url).then(response => {
                this.recommendJobList = response.data;
            }).catch(error => { });
        },
        getLatestJobList() {
            var url = host + 'recruits/search/latest/'
            axios.get(url).then(response => {
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