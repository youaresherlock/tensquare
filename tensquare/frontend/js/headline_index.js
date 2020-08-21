var vm = new Vue({
    el: "#app",
    data: {
        channels: [],
        articles: [],
        token: localStorage.token,
        clickIndex: -1,
        clickId:-1,
        activityList: [],
        problemList: [],
        page:1,
        moreTips:'点击获取下一页'
    },
    mounted() {
        this.getchannels();
        this.getArticles();
        this.getActivity();
        this.get_problem();
    },
    methods: {
        getchannels() {
            var url = host + 'channels/'
            axios.get(url).then(response => {
                this.channels = response.data.results;
            }).catch(error => { });
        },
        channelClicked(id, index) {
            this.clickIndex = index;
            this.articles.splice(0,this.articles.length);
            console.log(this.articles.length)
            this.page = 1;
            this.moreTips = '点击获取下一页'
            this.clickId = id;
            this.getArticles();
        },
        clickHot() {
            this.clickIndex = -1;
            this.clickId = -1;
            this.page = 1;
            this.moreTips = '点击获取下一页'
            this.articles.splice(0,this.articles.length);
            this.getArticles();
        },
        getArticles() {
            var url = host + 'article/' + this.clickId + '/channel/?page='+this.page
            axios.get(url).then(response => {
                for (var i = 0; i < response.data.results.length; i++) {
                    if (localStorage.id && response.data.results[i].collected_users.indexOf(parseInt(localStorage.id)) != -1) {
                        response.data.results[i].collected = true;
                    }
                    this.articles.push(response.data.results[i])
                }
                if(!response.data.next){
                    this.moreTips = '已加载全部数据'
                }
            }).catch(error => { });
        },
        getMore(){
            this.page = this.page + 1;
            this.getArticles();
        },
        getActivity() {
            var url = host + 'gatherings/'
            axios.get(url).then(response => {
                this.activityList = response.data.results;

            }).catch(error => { });
        },
        get_problem() {
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
        collect(articleid, index) {
            var url = host + 'article/' + articleid + '/collect/';
            axios.put(url, {}, {
                headers: {
                    'Authorization': 'JWT ' + this.token
                }
            }).then(response => {
                if (response.data.success) {
                    this.$message({
                        message: response.data.message,
                        type: 'success'
                    });

                    this.articles[index].collected = true;
                } else {
                    this.$message({
                        message: response.data.message,
                        type: 'error'
                    })
                }
            }).catch(error => {
                this.$message({
                    message: '操作失败,请重新登录',
                    type: 'error'
                });
            });
        },
        cancel_collect(articleid, index) {
            var url = host + 'article/' + articleid + '/collect/';
            axios.put(url, {}, {
                headers: {
                    'Authorization': 'JWT ' + this.token
                }
            }).then(response => {
                if (response.data.success) {
                    this.$message({
                        message: response.data.message,
                        type: 'success'
                    })
                    this.articles[index].collected = false;
                } else {
                    this.$message({
                        message: response.data.message,
                        type: 'error'
                    })
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