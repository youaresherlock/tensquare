var vm = new Vue({
    el: "#app",
    data: {
        showLogin: true,
        log_username: '',
        log_password: '',
        log_remember: true,
        titleTagList: [],
        hotTagList: [],
        problemList: [],
        tabIndex: -1,
        problemType: 1,
        token: localStorage.token
    },
    mounted() {
        this.getTitleTag();
        this.getAllProblems();
        if (localStorage.token) {
            this.showLogin = false;
        } else {
            this.showLogin = true;
        }
    },
    methods: {
        getTitleTag() {
            var url1 = host + 'labels/users/';
            axios.get(url1,{
                headers: {
                    'Authorization': 'JWT ' + this.token
                }
            }).then(response => {
                this.titleTagList = response.data;
            }).catch(error => { });
            var url2 = host + 'labels/';
            axios.get(url2).then(response => {
                this.hotTagList = response.data;
            }).catch(error => { });
        },
        getAllProblems() {
            var labelid = -1;
            if (this.tabIndex != -1) {
                labelid = this.titleTagList[this.tabIndex].id;
            }
            var type = 'new';
            if (this.problemType == 2) {
                type = 'hot'
            } else if (this.problemType == 3) {
                type = 'wait'
            }

            var url = host + 'questions/' + labelid + '/label/' + type + '/'
            axios.get(url).then(response => {
                this.problemList = response.data;
            }).catch(error => { });
        },
        login() {
            if (this.log_username == '') {
                this.$message({
                    message: '请输入用户名',
                    type: "error"
                })
                return
            }
            if (this.log_password == '') {
                this.$message({
                    message: '请输入密码',
                    type: "error"
                })
                return
            }
            var url = host + 'authorizations/';
            axios.post(url,
                {
                    username: this.log_username,
                    password: this.log_password,

                }
            ).then(res => {
                this.setUser(res.data.token, res.data.username, res.data.avatar, res.data.id)
                this.$message({
                    message: '登录成功',
                    type: "success"
                })
                setTimeout(() => {
                    location.reload();
                }, 2000);

            }).catch(error => {
                this.$message({
                    message: '登录失败',
                    type: "error"
                })
            });
        },
        tabChange(index) {
            this.tabIndex = index;
            this.problemType = 1;
            this.getAllProblems();
        },
        problemTypeChange(type) {
            this.problemType = type;
            this.getAllProblems();
        },
        setUser(token, username, avatar, id) {
            localStorage.token = token;
            localStorage.username = username;
            localStorage.avatar = avatar;
            localStorage.id = id
        },
    },
});