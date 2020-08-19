// 后端接口地址
var host = 'http://127.0.0.1:8000/';

// 获取查询字符串数据
function get_query_string(name) {
    var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
    var r = window.location.search.substr(1).match(reg);
    if (r != null) {
        return decodeURI(r[2]);
    }
    return null;
}

// 格式化日期 包含了星期的显示
function formatTimeContainsWeek(strTime) {
    var tempDate = new Date(strTime);
    var year = tempDate.getFullYear();
    var month = tempDate.getMonth() + 1;
    var dates = tempDate.getDate();
    var arr = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
    var day = tempDate.getDay();
    if (month < 10) {
        month = '0' + month;
    }
    if (dates < 10) {
        dates = '0' + dates;
    }
    return year + '-' + month + '-' + dates + ' ' + arr[day]
}
// 格式化日期 包含了星期、时、分的显示
function formatTimeContainsWeekHourMinute(strTime) {
    var tempDate = new Date(strTime);
    var year = tempDate.getFullYear();
    var month = tempDate.getMonth() + 1;
    var dates = tempDate.getDate();
    var arr = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
    var day = tempDate.getDay();
    if (month < 10) {
        month = '0' + month;
    }
    if (dates < 10) {
        dates = '0' + dates;
    }
    var h = tempDate.getHours();
    h = h < 10 ? '0' + h : h;
    var m = tempDate.getMinutes();
    m = m < 10 ? '0' + m : m;

    return year + '-' + month + '-' + dates + ' ' + h + ':' + m + ' ' + arr[day]
}
// 格式化日期， 只有年月日
function formatTime(strTime) {
    var tempDate = new Date(strTime);
    var year = tempDate.getFullYear();
    var month = tempDate.getMonth() + 1;
    var dates = tempDate.getDate();
    if (month < 10) {
        month = '0' + month;
    }
    if (dates < 10) {
        dates = '0' + dates;
    }
    return year + '-' + month + '-' + dates + ' '
}
// 格式化日期
function formatTime2(strTime) {
    var tempDate = new Date(strTime);
    var year = tempDate.getFullYear();
    var month = tempDate.getMonth() + 1;
    var dates = tempDate.getDate();
    if (month < 10) {
        month = '0' + month;
    }
    if (dates < 10) {
        dates = '0' + dates;
    }
    var h = tempDate.getHours();
    h = h < 10 ? '0' + h : h;
    var m = tempDate.getMinutes();
    m = m < 10 ? '0' + m : m;
    return year + '-' + month + '-' + dates + ' ' + h + ':' + m + ' '
}

function calculatDurationDisplay(strTime) {
    var tempDate = +new Date(strTime);
    var now = +new Date();
    var duration = Math.abs(tempDate - now) / 1000;
    var days = Math.floor(duration / 60 / 60 / 24);
    if (Math.abs(days) < 1) {
        var hours = Math.floor(duration / 60 / 60);
        if (Math.abs(hours) < 1) {
            var minutes = Math.floor(duration / 60);
            if (Math.abs(minutes) < 1) {
                return Math.floor(duration) + '秒'
            } else {
                return minutes + '分钟'
            }
        } else {
            return hours + '小时'
        }
    } else {
        return days + '天'
    }
}

function calculatDuration(strTime) {
    var tempDate = +new Date(strTime);
    var now = +new Date();
    var duration = (tempDate - now) / 1000;
    return Math.floor(duration);
}

window.onload = function () {
    var header = document.querySelector('header');
    header.innerHTML = '\
    <div class="sui-navbar">\
        <div class="navbar-inner">\
        <a href="./index.html" class="sui-brand">\
            <img src="./img/asset-logo-black.png" alt="社交" />\
        </a>\
        <ul class="sui-nav">\
            <li>\
            <a href="./index.html">头条</a>\
            </li>\
            <li>\
            <a href="./qa-index.html">问答</a>\
            </li>\
            <li>\
            <a href="./activity-index.html">活动</a>\
            </li>\
            <li>\
            <a href="./spit-index.html">吐槽</a>\
            </li>\
            <li>\
            <a href="./recruit-index.html">招聘</a>\
            </li>\
        </ul>\
        <form id="search" class="sui-form sui-form pull-left" style="display:none">\
            <input type="text" placeholder="输入关键词..." id="keyword"/>\
            <span class="btn-search fa fa-search" id="searchBtn"></span>\
        </form>\
        <div class="sui-nav pull-right info" id="userstatus" >\
            <li>\
            <a href="./person-loginsign.html" target="_blank" style="font-size:12px">注册</a>\
            </li>\
            <li>\
            <a href="./person-loginsign.html" target="_blank" class="sui-btn btn-login" style="font-size:12px">登录</a>\
            </li>\
        </div>\
        </div>\
    </div>';
    var lis = document.querySelectorAll('header .sui-nav > li');
    var search = document.querySelector('#search');
    if (location.pathname == '/' || location.pathname == "/index.html" || location.pathname.indexOf('headline') != -1 || location.pathname.indexOf('search') != -1) {
        lis[0].classList.add('active');
        search.style.display = 'block';
    } else if (location.pathname.indexOf('qa') != -1) {
        lis[1].classList.add('active');
    } else if (location.pathname.indexOf('activity') != -1) {
        lis[2].classList.add('active');
    } else if (location.pathname.indexOf('spit') != -1) {
        lis[3].classList.add('active');
    } else if (location.pathname.indexOf('recruit') != -1) {
        lis[4].classList.add('active');
    }
    var token = localStorage.token
    if (token) {
        var userstatus = document.querySelector('#userstatus');
        var avatar_url = localStorage.avatar == 'null' ? './img/widget-photo.png' : localStorage.avatar;
        userstatus.innerHTML = '\
        <li>\
          <a href="./person-myfile.html" target="_blank" class="notice">'+ localStorage.username + '</a>\
        </li>\
        <li>\
        <a href="./person-myfile.html" target="_blank" class="homego">\
          <img src="'+ avatar_url + '" alt="用户头像" style="width:50px;height:50px"/>\
        </a>\
      </li>';
    }

    var searchBtn = document.querySelector('#searchBtn');
    var keyword = document.querySelector('#keyword')
    searchBtn.onclick = function () {
        if (keyword.value == "") {
            alert('请输入关键字');
            return;
        }
        location.href = '/search.html?keyword=' + keyword.value;
    }
}
