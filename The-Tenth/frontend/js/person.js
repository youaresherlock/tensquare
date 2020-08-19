var vm = new Vue({
    el: "#app",
    data: {
        show_profile_edit: false,
        show_mask: false,
        show_jishu_edit: false,
        clickType: 0,
        focusType: 1,
        collectType: 0,
        user: {
            replies: [],
            problems: [],
            focusQuestions: [],
            focusLabels: [],
            collectArticles: [],
            collectEnterprise: [],
            collectSpits: []
        },
        realname: '',
        birthday: '',
        mobile: '',
        city: '',
        sex: '',
        website: '',
        email: '',
        address: '',
        interest: [],
        interestid: [],
        choose_interestid: [],
        choose_interestname: [],
        token: sessionStorage.token || localStorage.token,
        allLabels: [],
        showalllabels: false,
        show_edit_pwd: false,
        new_pwd: ''

    },
    mounted() {
        this.getUserDetail();
        this.getLabels();
    },
    methods: {
        getLabels() {
            var url = host + 'labels/';
            axios.get(url).then(response => {
                this.allLabels = response.data;
            }).catch(error => { });
        },
        getUserDetail() {
            var token = localStorage.token
            if (token && token != "null") {
                var url = host + 'user/'
                axios.get(url, {
                    headers: {
                        'Authorization': 'JWT ' + token
                    }
                }).then(response => {
                    this.user = response.data;
                    this.realname = response.data.realname;
                    this.birthday = response.data.birthday;
                    this.sex = response.data.sex;
                    this.website = response.data.website;
                    this.city = response.data.city;
                    this.mobile = response.data.mobile;
                    this.email = response.data.email;
                    this.address = response.data.address;

                    for (var i = 0; i < response.data.labels.length; i++) {
                        this.interest.push(response.data.labels[i].label_name)
                        this.choose_interestid.push(response.data.labels[i].id)
                        this.interestid.push(response.data.labels[i].id)
                        this.choose_interestname.push(response.data.labels[i].label_name)
                    }

                }).catch(error => {
                    location.href = '/person-loginsign.html';
                });
            } else {
                location.href = '/person-loginsign.html';
            }
        },
        save_pwd() {
            if (this.new_pwd == '') {
                this.$message({
                    message: '密码不允许为空',
                    type: 'error'
                })
                return;
            }
            var url = host + 'user/password/';
            axios.put(
                url,
                {
                    password: this.new_pwd,
                },
                {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    }
                }).then(response => {
                    this.$message({
                        message: '修改成功~',
                        type: 'success'
                    })
                    this.show_edit_pwd = false;
                }).catch(error => {
                    this.$message({
                        message: '修改失败~',
                        type: 'error'
                    })
                });
        },
        saveLabel() {
            var url = host + 'user/label/'
            axios.put(
                url,
                {
                    labels: this.choose_interestid
                },
                {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    }
                }).then(response => {
                    this.show_mask = false;
                    this.show_jishu_edit = false;
                    this.$message({
                        message: '修改成功~',
                        type: 'success'
                    })
                    setTimeout(function () {
                        location.reload();
                    }, 1000);
                }).catch(error => {
                    this.$message({
                        message: '修改失败~',
                        type: 'error'
                    })
                });
        },
        clickLabel(id, labelname) {
            var tempIndex = this.choose_interestid.indexOf(id);
            if (tempIndex == -1) {
                this.choose_interestid.push(id);
                this.choose_interestname.push(labelname);
            } else {
                this.choose_interestid.splice(tempIndex, 1);
                this.choose_interestname.splice(tempIndex, 1)
            }

        },
        saveDetail() {
            var url = host + 'user/'
            axios.put(
                url,
                {
                    realname: this.realname,
                    sex: this.sex,
                    birthday: this.birthday,
                    website: this.website,
                    mobile: this.mobile,
                    email: this.email,
                    city: this.city,
                    address: this.address,
                    avatar: this.user.avatar
                },
                {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    }
                }).then(response => {
                    this.show_mask = false;
                    this.show_profile_edit = false;
                    // 更新头像
                    localStorage.avatar = this.user.avatar
                    this.$message({
                        message: '修改成功~',
                        type: 'success'
                    })
                    setTimeout(function () {
                        location.reload();
                    }, 1000);
                }).catch(error => {
                    this.$message({
                        message: '修改失败~',
                        type: 'error'
                    })
                });
        },
        uploadImg() {
            var reader = new FileReader();
            var file = document.querySelector("#myFile").files;
            reader.readAsDataURL(file[0]);
            reader.onload = () => {
                this.user.avatar = reader.result;
                var url = host + 'upload/avatar/'
                let formData = new FormData();
                formData.append('img', file[0])
                axios.post(url, formData, {
                    'Content-Type': 'multipart/form-data'
                }).then(res => {
                    this.user.avatar = res.data.imgurl;
                })
            }
        },
        logout() {
            localStorage.removeItem('id');
            localStorage.removeItem("username")
            localStorage.removeItem("token")
            localStorage.removeItem("avatar")
            location.href = "/person-loginsign.html"
        }

    },
});