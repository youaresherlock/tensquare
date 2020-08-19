var vm = new Vue({
    el: "#app",
    data: {
        item: {
        },
        token: localStorage.token,
        hasjoin: false
    },
    mounted() {
        var id = get_query_string("id");
        this.getActivityDetail(id);
    },
    methods: {
        getActivityDetail(id) {
            var url = host + 'gatherings/' + id + '/'
            axios.get(url).then(response => {
                this.item = response.data;
                if (localStorage.id) {
                    if (this.item.users.indexOf(parseInt(localStorage.id)) != -1) {
                        this.hasjoin = true;
                    } else {
                        this.hasjoin = false;
                    }
                }
            }).catch(error => { });

        },
        join(id) {
            var url = host + 'gatherings/' + id + '/join/'
            axios.post(url,
                {}, {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    responseType: 'json',
                }
            ).then(response => {
                if (response.data.success) {
                    this.$message({
                        message: response.data.message,
                        type: 'success'
                    });
                    this.hasjoin = !this.hasjoin;
                } else {
                    console.log('error')
                    this.$message({
                        message: response.data.message,
                        type: 'error'
                    });
                }

            }).catch(error => {
                this.$message({
                    message: '操作失败,请重试登录~',
                    type: 'error'
                })
            });
        }
    },
});