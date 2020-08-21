var vm = new Vue({
    el: "#app",
    data: {
        item: {
            logo: '',
            name: '',
            enterprise: {
                recruits: []
            },
            users: []
        },
        recruitLabels: [],
        enterpriseLabels: [],
        token: localStorage.token,
        collected: false,
        collect_count: 0
    },
    mounted() {
        var id = get_query_string('id');
        this.getJobDetail(id);
        this.addJobVisit(id);
    },
    methods: {
        // 获取招聘信息详情
        getJobDetail(id) {
            var url = host + 'recruits/' + id + '/'
            axios.get(url).then(response => {
                this.item = response.data;
                this.recruitLabels = this.item.labels.split(' ');
                this.enterpriseLabels = this.item.enterprise.labels.split(' ')

                if (localStorage.id && this.item.users.indexOf(parseInt(localStorage.id)) != -1) {
                    this.collected = true;
                }
                this.collect_count = this.item.users.length;
            }).catch(error => { });
        },
        // 增加招聘信息访问量
        addJobVisit(id) {
            var url = host + 'recruits/' + id + '/visit/'
            axios.put(url);
        },
        // 收藏招聘信息
        collectJob(id) {
            var url = host + 'recruits/' + id + '/collect/'
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
                        message: '收藏成功',
                        type: 'success'
                    });
                    this.collected = true;
                    this.collect_count++
                } else {
                    this.$message({
                        message: response.data.message,
                        type: 'error'
                    });
                }

            }).catch(error => {
                this.$message({
                    message: '操作失败,请重新登录',
                    type: 'error'
                });
            });
        },
        cancelCollectJob(id) {
            var url = host + 'recruits/' + id + '/cancelcollect/'
            axios.post(url,
                {}, {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    responseType: 'json',
                }
            ).then(response => {
                console.log(response)
                if (response.data.success) {
                    this.$message({
                        message: '取消收藏成功',
                        type: 'success'
                    });
                    this.collected = false;
                    this.collect_count--;
                } else {
                    this.$message({
                        message: response.data.message,
                        type: 'error'
                    });
                }

            }).catch(error => {
                this.$message({
                    message: '操作失败,请重新登录',
                    type: 'error'
                });
            });
        },
    },
});