var vm = new Vue({
    el: "#app",
    data: {
        item: {},
        commentList: [],
        token: localStorage.token,
        show_txt: 'none',
        comment_txt: ''
    },
    mounted() {
        var id = get_query_string("id");
        this.getSpitDetail(id);
        this.getSpitCommentList(id);
    },
    methods: {
        getSpitDetail(id) {
            var url = host + 'spit/' + id + '/'
            axios.get(url, {
                headers: {
                    'Authorization': 'JWT ' + this.token
                }
            }).then(response => {
                this.item = response.data;
            }).catch(error => { });
        },
        getSpitCommentList(id) {
            var url = host + 'spit/' + id + '/children/'
            axios.get(url, {
                headers: {
                    'Authorization': 'JWT ' + this.token
                }
            }).then(response => {
                this.commentList = response.data
            }).catch(error => { });
        },
        thumbup(id) {
            var url = host + 'spit/' + id + '/updatethumbup/';
            axios.put(url, {}, {
                headers: {
                    'Authorization': 'JWT ' + this.token
                }
            }).then(response => {
                if (response.data.success) {
                    if (this.item.hasthumbup) {
                        this.item.thumbup--
                        this.item.hasthumbup = false
                        this.$message({
                            message: '取消点赞成功~',
                            type: 'success'
                        })
                    } else {
                        this.item.thumbup++
                        this.item.hasthumbup = true
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
        thumbuplistitem(id, index) {
            var url = host + 'spit/' + id + '/updatethumbup/';
            axios.put(url, {}, {
                headers: {
                    'Authorization': 'JWT ' + this.token
                }
            }).then(response => {
                if (response.data.success) {
                    if (this.commentList[index].hasthumbup) {
                        this.commentList[index].thumbup--
                        this.commentList[index].hasthumbup = false
                        this.$message({
                            message: '取消点赞成功~',
                            type: 'success'
                        })
                    } else {
                        this.commentList[index].thumbup++
                        this.commentList[index].hasthumbup = true
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
        publish_spit(parent_id) {
            var content = this.comment_txt;
            if (content == '') {
                this.$message({
                    message: '内容不允许为空',
                    type: 'error'
                })
            }
            var url = host + 'spit/'
            axios.post(url, {
                content: content,
                parent: this.item.id
            }, {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    }
                }).then(response => {
                    this.$message({
                        message: '评论成功~',
                        type: 'success'
                    })
                    this.show_txt = 'none'
                    setTimeout(function () {
                        location.reload()
                    }, 1000)

                }).catch(error => {
                    this.$message({
                        message: "评论失败,请重新登录...",
                        type: 'error'
                    })
                });
        }
    },
});