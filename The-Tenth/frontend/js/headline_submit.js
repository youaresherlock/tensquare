var url = host + 'channels/'
var channelContainer = document.querySelector('#menu12');
var selectedChannel = null;
var selectNameElt = document.querySelector('.dropdown-inner #drop12 span');
var channelAElt = document.querySelector('.dropdown-inner #drop12');
channelAElt.onclick = function () {
    if (channelContainer.offsetWidth) {
        channelContainer.style.display = 'none';
    } else {
        channelContainer.style.display = 'block';
    }

};
axios.get(url).then(response => {
    console.log(response)
    var channels = response.data.results;
    var htmlStr = "";
    for (var i = 0; i < channels.length; i++) {
        var channel = channels[i];
        htmlStr += '<li role="presentation">\
                        <a role="menuitem" tabindex="'+ i + '" href="javascript:void(0);" data-value="' + channel.id + '">' + channel.name + '</a>\
                    </li>';

    }
    selectedChannel = channels[0].id;
    selectNameElt.innerHTML = channels[0].name;
    channelContainer.innerHTML = htmlStr

    var lis = channelContainer.querySelectorAll('li a');
    for (var i = 0; i < lis.length; i++) {
        lis[i].onclick = function () {
            selectedChannel = this.getAttribute('data-value');
            selectNameElt.innerHTML = this.innerHTML;
            channelContainer.style.display = 'none';
        }
    }

}).catch(error => { });

var ulTagContainer = document.querySelector('.tags-area .tags-box ul');
var idTags = document.querySelector('.tags-area #tags');
var url = host + 'labels/'
var chooseIds = [];
var chooseName = [];
axios.get(url).then(response => {

    var hotTagList = response.data;
    var html_str = '';
    for (var i = 0; i < hotTagList.length; i++) {
        html_str += '<li class="tag-item" data-label-id="' + hotTagList[i].id + '">' + hotTagList[i].label_name + '</li>'
    }
    ulTagContainer.innerHTML = html_str;
    var lis = document.querySelectorAll('.tag-item')
    for (var i = 0; i < lis.length; i++) {
        lis[i].onclick = function () {
            var clickedId = parseInt(this.getAttribute('data-label-id'));
            var clickedName = this.innerHTML;
            var tempIndex = chooseIds.indexOf(clickedId);
            if (tempIndex == -1) {
                chooseIds.push(clickedId);
                chooseName.push(clickedName)
            } else {
                chooseIds.splice(tempIndex, 1);
                chooseName.splice(tempIndex, 1)

            }
            idTags.value = chooseName.join(" ")
        }
    }
}).catch(error => { });
var tags_box = document.querySelector('.tags-area .tags-box');
var tags_area = document.querySelector('.tags-area');
tags_area.onmouseover = function () {
    tags_box.style.display = 'block';
}
tags_box.onmouseout = function () {
    tags_box.style.display = 'none';
}
var articleImg = document.querySelector('#articleImg');
var thumbImg = document.querySelector('#thumbImg');
var articleImgUrl = '';
articleImg.onchange = function () {
    var url = host + 'upload/avatar/'
    let formData = new FormData();
    formData.append('img', articleImg.files[0])
    axios.post(url, formData, {
        'Content-Type': 'multipart/form-data'
    }).then(res => {
        articleImgUrl = res.data.imgurl;
        console.log(articleImgUrl)
        thumbImg.src = articleImgUrl;
        thumbImg.style.display = 'block';
    })
};
var vm = new Vue({
    el: "#app",
    data: {
        token: sessionStorage.token || localStorage.token,
    },
    mounted() {
    },
    methods: {
        submit_headline() {
            console.log('onclick...')
            var content = CKEDITOR.instances.editor1.getData()
            var title = document.querySelector('#inputTitle').value;
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
            if (!selectedChannel) {
                this.$message({
                    message: '请选择频道',
                    type: 'error'
                })
                return;
            }
            var url = host + 'article/'
            axios.post(url, {
                content: content,
                labels: chooseIds,
                title: title,
                channel: selectedChannel,
                image: articleImgUrl
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
                        location.href = '/headline-detail.html?id=' + response.data.articleid;
                    }, 1000);
                }).catch(error => {
                    this.$message({
                        message: "发布失败,请重新登录",
                        type: 'error'
                    })
                });
        }
    },
});