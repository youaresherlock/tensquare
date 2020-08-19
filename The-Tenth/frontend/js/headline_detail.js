var vm = new Vue({
    el: "#app",
    data: {
        token: sessionStorage.token || localStorage.token,
        articleDetail: {
            user: {},
        },
        collected: false,
        focused: false,
        comment: '',
        sub_comment: '',
        commentList: [],
        avatar: localStorage.avatar,
        replyId: -1,
        problemList: [],
    },
    mounted() {
        var id = get_query_string("id");
        this.get_article_detail(id);
        this.get_hot_problems();
    },
    methods: {
        get_hot_problems() {
            var labelid = -1;
            var type = 'hot';

            var url = host + 'questions/' + labelid + '/label/' + type + '/'
            axios.get(url).then(response => {
                this.problemList = response.data;
                if (this.problemList.length > 4) {
                    this.problemList.splice(4)
                }
            }).catch(error => { });
        },
        get_article_detail(id) {
            var url = host + 'article/' + id + '/'
            axios.get(url).then(response => {
                this.articleDetail = response.data;
                for (var i = 0; i < this.articleDetail.comments.length; i++) {
                    if (!this.articleDetail.comments[i].parent) {
                        this.commentList.push(this.articleDetail.comments[i])
                    }
                }
                if (localStorage.id && this.articleDetail.collected_users.indexOf(parseInt(localStorage.id)) != -1) {
                    this.collected = true;
                } else {
                    this.collected = false;
                }

                if (localStorage.id && this.articleDetail.user.fans.indexOf(parseInt(localStorage.id)) != -1) {
                    this.focused = true;
                } else {
                    this.focused = false;
                }
            }).catch(error => { });
        },
        collect() {
            var url = host + 'article/' + this.articleDetail.id + '/collect/';
            axios.put(url, {}, {
                headers: {
                    'Authorization': 'JWT ' + this.token
                }
            }).then(response => {
                if (response.data.success) {
                    this.collected = !this.collected

                    this.$message({
                        message: response.data.message,
                        type: 'success'
                    })
                } else {
                    this.$message({
                        message: response.data.message,
                        type: 'error'
                    })
                }
            }).catch(error => {
                this.$message({
                    message: "操作失败,请重新登录...",
                    type: 'error'
                })
            });
        },
        focus(userid) {
            var url = host + 'users/like/' + userid + '/';
            axios.post(url, {}, {
                headers: {
                    'Authorization': 'JWT ' + this.token
                }
            }).then(response => {
                if (response.data.success) {

                    this.focused = true
                    this.$message({
                        message: response.data.message,
                        type: 'success'
                    })
                } else {
                    this.$message({
                        message: response.data.message,
                        type: 'error'
                    })
                }
            }).catch(error => {
                this.$message({
                    message: "操作失败,请重新登录...",
                    type: 'error'
                })
            });
        },
        unfocus(userid) {
            var url = host + 'users/like/' + userid + '/';
            axios.delete(url, {
                headers: {
                    'Authorization': 'JWT ' + this.token
                }
            }).then(response => {
                if (response.data.success) {

                    this.focused = false
                    this.$message({
                        message: response.data.message,
                        type: 'success'
                    })
                } else {
                    this.$message({
                        message: response.data.message,
                        type: 'error'
                    })
                }
            }).catch(error => {
                this.$message({
                    message: "操作失败,请重新登录...",
                    type: 'error'
                })
            });
        },
        publish_comment() {
            if (this.comment == "") {
                this.$message({
                    message: '评论内容不允许为空',
                    type: 'error'
                })
                return;
            }

            var url = host + 'article/' + this.articleDetail.id + '/publish_comment/';
            axios.post(url, {
                article: this.articleDetail.id,
                content: this.comment
            }, {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    }
                }).then(response => {
                    if (response.data.success) {
                        this.$message({
                            message: response.data.message,
                            type: 'success'
                        })
                        this.comment = ''
                        setTimeout(function () {
                            location.reload();
                        }, 2000)
                    } else {
                        this.$message({
                            message: response.data.message,
                            type: 'error'
                        })
                    }
                }).catch(error => {
                    this.$message({
                        message: "操作失败,请重新登录...",
                        type: 'error'
                    })
                });
        },
        publish_sub_comment() {
            if (this.sub_comment == "") {
                this.$message({
                    message: '评论内容不允许为空1',
                    type: 'error'
                })
                return;
            }

            var url = host + 'article/' + this.articleDetail.id + '/publish_comment/';
            axios.post(url, {
                article: this.articleDetail.id,
                content: this.sub_comment,
                parent: this.replyId
            }, {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    }
                }).then(response => {
                    if (response.data.success) {
                        this.$message({
                            message: response.data.message,
                            type: 'success'
                        })
                        this.sub_comment = ''
                        setTimeout(function () {
                            location.reload();
                        }, 2000)
                    } else {
                        this.$message({
                            message: response.data.message,
                            type: 'error'
                        })
                    }
                }).catch(error => {
                    this.$message({
                        message: "操作失败,请重新登录...",
                        type: 'error'
                    })
                });
        }
    },
});