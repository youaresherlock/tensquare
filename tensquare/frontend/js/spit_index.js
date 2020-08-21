var vm = new Vue({
    el: "#app",
    data: {
        spitList: [],
        token: localStorage.token
    },
    mounted() {
        this.getSpitList();
    },
    methods: {
        getSpitList() {
            var url = host + 'spit/'
            axios.get(url, {
                headers: {
                    'Authorization': 'JWT ' + this.token
                }
            }).then(response => {
                this.spitList = response.data;
            }).catch(error => { });
        },
        thumbuplistitem(id, index) {
            var url = host + 'spit/' + id + '/updatethumbup/';
            axios.put(url, {}, {
                headers: {
                    'Authorization': 'JWT ' + this.token
                }
            }).then(response => {
                if (response.data.success) {
                    if (this.spitList[index].hasthumbup) {
                        this.spitList[index].thumbup--
                        this.spitList[index].hasthumbup = false
                        this.$message({
                            message: '取消点赞成功~',
                            type: 'success'
                        })
                    } else {
                        this.spitList[index].thumbup++
                        this.spitList[index].hasthumbup = true
                        this.$message({
                            message: '点赞成功~',
                            type: 'success'
                        })
                    }


                } else {
                    this.$message({
                        message: response.data.message,
                        type: 'error'
                    })
                }
            }).catch(error => {
                this.$message({
                    message: '操作失败,请重试登录~',
                    type: 'error'
                })
            });
        },
        collect(id, index) {
            var url = host + 'spit/' + id + '/collect/';
            axios.put(url, {}, {
                headers: {
                    'Authorization': 'JWT ' + this.token
                }
            }).then(response => {
                if (response.data.success) {
                    if (this.spitList[index].collected) {
                        this.spitList[index].collected = false;
                        this.$message({
                            message: '取消收藏成功~',
                            type: 'success'
                        })
                    } else {
                        this.spitList[index].collected = true;
                        this.$message({
                            message: '收藏成功~',
                            type: 'success'
                        })
                    }

                } else {
                    this.$message({
                        message: response.data.message,
                        type: 'error'
                    })
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