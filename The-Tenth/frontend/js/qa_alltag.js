var vm = new Vue({
    el: "#app",
    data: {
        tagList: [],
        token: localStorage.token
    },
    mounted() {
        this.getAllTag();
    },
    methods: {
        getAllTag() {
            var url = host + 'labels/full/'
            axios.get(url).then(response => {
                for (var i = 0; i < response.data.length; i++) {
                    var tag = response.data[i];
                    tag.focus_count = tag.users.length;
                    if (localStorage.id && tag.users.indexOf(parseInt(localStorage.id)) != -1) {
                        tag.has_focus = true;
                    } else {
                        tag.has_focus = false;
                    }
                    this.tagList.push(tag)
                }
            }).catch(error => { });
        },
        focusin_tag(id, index) {
            var url = host + 'labels/' + id + '/focusin/';
            axios.put(url, {}, {
                headers: {
                    'Authorization': 'JWT ' + this.token
                }
            }).then(response => {
                if (response.data.success) {
                    this.$message({
                        message: '操作成功~',
                        type: 'success'
                    })
                    this.tagList[index].has_focus = true;
                    this.tagList[index].focus_count++;
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
        focusout_tag(id, index) {
            var url = host + 'labels/' + id + '/focusout/';
            axios.put(url, {}, {
                headers: {
                    'Authorization': 'JWT ' + this.token
                }
            }).then(response => {
                if (response.data.success) {
                    this.$message({
                        message: '操作成功~',
                        type: 'success'
                    })
                    this.tagList[index].has_focus = false;
                    this.tagList[index].focus_count--;
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
    },
});
