var vm = new Vue({
    el: "#app",
    data: {
        token: localStorage.token
    },
    mounted() {
    },
    methods: {
        publish_qa() {
            var content = CKEDITOR.instances.editor2.getData()
            var title = document.querySelector('#qa_title').value;
            if (title == '') {
                this.$message({
                    message: '标题不允许为空',
                    type: 'error'
                })
                return;
            }
            if (content == '') {
                this.$message({
                    message: '内容不允许为空',
                    type: 'error'
                })
                return;
            }
            if (chooseIds.length == 0) {
                this.$message({
                    message: '请选择标签',
                    type: 'error'
                })
                return;
            }
            var url = host + 'questions/'
            axios.post(url,
                {
                    content: content,
                    labels: chooseIds,
                    title: title
                }, {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    }
                }).then(response => {
                    this.$message({
                        message: '发布成功~',
                        type: 'success'
                    })
                    setTimeout(function () {
                        location.href = '/qa-index.html'
                    }, 1000);
                }).catch(error => {
                    this.$message({
                        message: "发布失败,请重试登录",
                        type: 'error'
                    })
                });
        }
    },
});