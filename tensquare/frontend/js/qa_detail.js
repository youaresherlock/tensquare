var vm = new Vue({
    el: "#app",
    data: {
        problemItem: {},
        problem_list: [],
        show_comment: false,
        show_comment_index: -1,
        problem_content: '',
        token: localStorage.token,
        answer_content:''
    },
    mounted() {
        var id = get_query_string("id");
        this.get_problem_detail(id);
    },
    methods: {
        answer(){
            if (this.answer_content == '') {
                this.$message({
                    message: '请填写回答内容',
                    type: 'error'
                })
                return;
            }
            var url = host + 'reply/';
            axios.post(url, {
                problem: this.problemItem.id,
                content: this.answer_content,
                type:2
            }, {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    }
                }).then(response => {
                    console.log(response)
                    this.$message({
                        message: '回答成功~',
                        type: 'success'
                    })
                    setTimeout(function () {
                        location.reload();
                    }, 1000);
                }).catch(error => {
                    this.$message({
                        message: "评论失败",
                        type: 'error'
                    })
                });
        },
        get_problem_detail(id) {

            var url = host + 'questions/' + id + '/'
            axios.get(url).then(response => {
                this.problemItem = response.data;
                this.get_similar(-1);
            }).catch(error => { });
        },
        get_similar(labelid) {
            var url = host + 'questions/' + labelid + '/label/hot/'
            axios.get(url).then(response => {
                this.problem_list = response.data;
            }).catch(error => { });
        },
        publish_comment() {
            if (this.problem_content == '') {
                this.$message({
                    message: '请填写评论内容',
                    type: 'error'
                })
                return;
            }
            var url = host + 'reply/';
            axios.post(url, {
                problem: this.problemItem.id,
                content: this.problem_content,
                type:0
            }, {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    }
                }).then(response => {
                    console.log(response)
                    this.$message({
                        message: '评论成功~',
                        type: 'success'
                    })
                    setTimeout(function () {
                        location.reload();
                    }, 1000);
                }).catch(error => {
                    this.$message({
                        message: "评论失败",
                        type: 'error'
                    })
                });
        },
        publish_comment_reply() {
            if (this.problem_content == '') {
                this.$message({
                    message: '请填写评论内容',
                    type: 'error'
                })
                return;
            }
            var url = host + 'reply/';
            axios.post(url, {
                problem: this.problemItem.id,
                parent: this.problemItem.answer_question[this.show_comment_index].id,
                content: this.problem_content,
                type:1
            }, {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    }
                }).then(response => {
                    console.log(response)
                    this.$message({
                        message: '评论成功~',
                        type: 'success'
                    })
                    setTimeout(function () {
                        location.reload();
                    }, 1000);
                }).catch(error => {
                    this.$message({
                        message: "评论失败",
                        type: 'error'
                    })
                });
        },
        thumbup_problem() {
            var url = host + 'questions/' + this.problemItem.id + '/useful/';
            axios.put(url, {}, {
                headers: {
                    'Authorization': 'JWT ' + this.token
                }
            }).then(response => {
                if (response.data.success) {

                    this.problemItem.useful_count++
                    this.$message({
                        message: '操作成功~',
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
                    message: '操作失败,请重试登录~',
                    type: 'error'
                })
            });

        },
        thumbdown_problem() {
            var url = host + 'questions/' + this.problemItem.id + '/unuseful/';
            axios.put(url, {}, {
                headers: {
                    'Authorization': 'JWT ' + this.token
                }
            }).then(response => {
                if (response.data.success) {

                    this.problemItem.unuseful_count++
                    this.$message({
                        message: '操作成功~',
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
                    message: '操作失败,请重试登录~',
                    type: 'error'
                })
            });
        },
        thumbup_reply(id, index) {

            var url = host + 'reply/' + id + '/useful/';
            axios.put(url, {}, {
                headers: {
                    'Authorization': 'JWT ' + this.token
                }
            }).then(response => {
                if (response.data.success) {
                    this.problemItem.answer_question[index].useful_count++
                    this.$message({
                        message: '操作成功~',
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
                    message: '操作失败,请重试登录~',
                    type: 'error'
                })
            });
        },
        thumbdown_reply(id, index) {
            var url = host + 'reply/' + id + '/unuseful/';
            axios.put(url, {}, {
                headers: {
                    'Authorization': 'JWT ' + this.token
                }
            }).then(response => {
                if (response.data.success) {

                    this.problemItem.answer_question[index].unuseful_count++
                    this.$message({
                        message: '操作成功~',
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
                    message: '操作失败,请重试登录~',
                    type: 'error'
                })
            });
        }
    },
});