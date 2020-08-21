var vm = new Vue({
    el: "#app",
    data: {
        reg_username: '',
        code: '',
        reg_mobile: '',
        reg_password: '',
        reg_allow: true,
        log_username: '',
        log_password: '',
        log_remember: true,
        send_flag: false,
        remain_seconds: 60
    },
    mounted() {
        var obj = new WxLogin({
            id: "weixin",
            appid: "wx3bdb1192c22883f3",
            scope: "snsapi_login",
            redirect_uri: "http://note.java.itcast.cn/weixinlogin.html"
        });
    },
    methods: {
        sendSMS() {
            if (this.reg_mobile == '') {
                this.$message({
                    message: '请输入手机号码',
                    type: "error"
                })
                return
            }
            var url = host + 'sms_codes/' + this.reg_mobile + '/';

            axios.get(url).then(res => {
                if (res.data.success) {
                    alert('测试阶段,短信验证码为:'+res.data.sms_code);
                    this.send_flag = true;
                    var timerid = setInterval(() => {
                        this.remain_seconds--;
                        if (this.remain_seconds == 0) {
                            clearInterval(timerid);
                            this.send_flag = false;
                            this.remain_seconds = 60;
                        }
                    }, 1000);
                } else {
                    this.$message({
                        message: res.data.message,
                        type: 'error'
                    })
                }

            }).catch(error => {
                if (error.response) {
                    this.$message({
                        message: error.response.data.message,
                        type: "error"
                    })
                }
            });
        },
        register() {
            if (this.reg_username == '') {
                this.$message({
                    message: '请输入用户名',
                    type: "error"
                })
                return
            }
            if (this.reg_mobile == '') {
                this.$message({
                    message: '请输入手机号码',
                    type: "error"
                })
                return
            }
            if (this.reg_password == '') {
                this.$message({
                    message: '请输入密码',
                    type: "error"
                })
                return
            }
            if (this.code == '') {
                this.$message({
                    message: '请输入短信验证码',
                    type: "error"
                })
                return
            }
            if (!this.reg_allow) {
                this.$message({
                    message: '请勾同意协议',
                    type: "error"
                })
                return
            }

            var url = host + 'users/';
            axios.post(url,
                {
                    username: this.reg_username,
                    password: this.reg_password,
                    mobile: this.reg_mobile,
                    sms_code: this.code
                }
            ).then(res => {
                this.$message({
                    message: "注册成功",
                    type: 'success'
                })
                localStorage.setItem('id', res.data.id)
                localStorage.setItem("username", res.data.username)
                localStorage.setItem("token", res.data.token)
                localStorage.setItem("avatar", res.data.avatar)

                setTimeout(function () {
                    location.href = '/'
                }, 2000)
            }).catch(error => {
                if (error.response) {
                    this.$message({
                        message: error.response.data,
                        type: "error"
                    })
                }
            });
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
                this.$message({
                    message: '登录成功',
                    type: "success"
                })
                localStorage.setItem('id', res.data.id)
                localStorage.setItem("username", res.data.username)
                localStorage.setItem("token", res.data.token)
                localStorage.setItem("avatar", res.data.avatar)
                setTimeout(function () {
                    location.href = "/person-myfile.html"
                }, 2000)

            }).catch(error => {
                this.$message({
                    message: '用户名或者密码错误,请重新尝试',
                    type: "error"
                })
            });
        }
    },
});