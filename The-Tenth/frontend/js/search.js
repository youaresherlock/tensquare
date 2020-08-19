var vm = new Vue({
    el: "#app",
    data: {
        articles: [],
        token: localStorage.token,
        keyword: ''

    },
    mounted() {
        this.keyword = get_query_string("keyword");
        this.getArticles(this.keyword);
    },
    methods: {
        getArticles(keyword) {
            var url = host + 'articles/search/?text=' + keyword;
            axios.get(url).then(response => {
                this.articles = response.data.results;
                console.log(response)
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