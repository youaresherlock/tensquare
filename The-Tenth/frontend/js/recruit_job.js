var vm = new Vue({
    el: "#app",
    data: {
        item: {
            users: []
        },
        recruits: [],
        enterpriseLabels: [],
        flag: 1,
        token: localStorage.token,
        collected: false,
        collect_count: 0
    },
    mounted() {
        var id = get_query_string('id');
        this.addEnterpriseVisit(id);
        this.getEnterpriseDetail(id);
    },
    methods: {
        // 增加公司访问量
        addEnterpriseVisit(id) {
            var url = host + 'enterprise/' + id + '/visit/'
            axios.put(url);
        },
        // 获取公司详情
        getEnterpriseDetail(id) {
            var url = host + 'enterprise/' + id + '/'
            axios.get(url).then(response => {
                this.item = response.data;
                this.enterpriseLabels = this.item.labels.split(' ');
                this.recruits = this.item.recruits;
                this.collect_count = this.item.users.length;
                if (localStorage.id && this.item.users.indexOf(parseInt(localStorage.id)) != -1) {
                    this.collected = true;
                }
            });
        },
        // 收藏公司
        collectEnterprise(id) {
            var url = host + 'enterprise/' + id + '/collect/'
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
                        message: '收藏公司成功',
                        type: 'success'
                    });
                    this.collect_count++;
                    this.collected = true;
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
        // 取消收藏公司
        cancelCollectEnterprise(id) {
            var url = host + 'enterprise/' + id + '/cancelcollect/'
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
                        message: '取消收藏公司成功',
                        type: 'success'
                    });
                    this.collect_count--;
                    this.collected = false;
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