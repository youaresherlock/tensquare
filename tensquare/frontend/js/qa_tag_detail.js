var vm = new Vue({
    el: "#app",
    data: {
        tagDetail: {},
        hotTagList: [],
        token: localStorage.token,
        tabindex: 1,
        labelRecruits: []
    },
    mounted() {
        var id = get_query_string('id');
        this.getTagDetail(id);
        this.getTitleTag();
    },
    methods: {
        getTitleTag() {
            var url = host + 'labels/'
            axios.get(url).then(response => {
                this.hotTagList = response.data;
            }).catch(error => { });

        },
        searchJob(keyword) {
            var url = host + 'recruits/search/city/keyword/'
            axios.post(url, {
                keyword: keyword
            }).then(response => {
                console.log(response.data)
                this.labelRecruits = response.data;
            }).catch(error => { });
        },
        getTagDetail(id) {
            var url = host + 'labels/' + id + '/'
            axios.get(url).then(response => {
                if (localStorage.id && response.data.users.indexOf(parseInt(localStorage.id)) != -1) {
                    response.data.has_focus = true;
                } else {
                    response.data.has_focus = false;
                }
                this.tagDetail = response.data
                this.searchJob(this.tagDetail.label_name);
            }).catch(error => { });
        },
        focus_in() {
            var url = host + 'labels/' + this.tagDetail.id + '/focusin/';
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
                    this.tagDetail.has_focus = true;
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
        focus_out() {
            var url = host + 'labels/' + this.tagDetail.id + '/focusout/';
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
                    this.tagDetail.has_focus = false;
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
