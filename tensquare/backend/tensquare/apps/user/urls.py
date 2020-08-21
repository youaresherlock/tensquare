from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from user import views

urlpatterns = [
    # 注册用户
    url(r'^users/$', views.UserCreateView.as_view()),
    # 登录认证
    url(r'^authorizations/$', obtain_jwt_token),
    # 修改密码
    url(r'^user/password/$', views.UserPwdView.as_view()),
    # 修改擅长技术
    url(r'^user/label/$', views.UserLabelView.as_view()),
    # 查询用户详情
    url(r'^user/$', views.UserDetailView.as_view()),
    # 关注和取消关注
    url(r'^users/like/(?P<userid>[^/.]+)/$', views.UserLikeView.as_view()),
    # 微信登陆
    url(r'^weixin/user/$', views.WeixinAuthUserView.as_view()),
]