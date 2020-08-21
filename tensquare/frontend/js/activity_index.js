var vm = new Vue({
    el: "#app",
    data: {
        activityList: [],
        token: sessionStorage.token || localStorage.token
    },
    mounted() {
        this.getActivityList();
    },
    methods: {
        getActivityList() {
            var url = host + 'gatherings/'
            axios.get(url).then(response => {
                this.activityList = response.data.results;
                for (var i = 0; i < this.activityList.length; i++) {
                    var activity = this.activityList[i];
                    if (localStorage.id) {
                        if (activity.users.indexOf(parseInt(localStorage.id)) != -1) {
                            activity.join = true;
                        }
                    }
                }

            }).catch(error => { });
        }
    },
});