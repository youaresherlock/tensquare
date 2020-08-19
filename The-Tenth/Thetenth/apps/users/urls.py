from django.urls import path, re_path


from apps.users.views import verifications, users, userinfo

urlpatterns = [
    # 注册获取短信验证码的子路由
    re_path(r'^sms_codes/(?P<mobile>\d+)/$', verifications.VerificationsView.as_view()),
    # 注册用户注册的子路由
    path('users/', users.RegisterUserView.as_view()),
    # 注册用户登录的子路由
    path('authorizations/', users.LoginUserView.as_view()),
    # 注册获取更改用户信息的子路由
    path('user/', userinfo.UserInfoView.as_view()),
    # 注册修改用户密码的子路由
    path('user/password/', userinfo.ChangePasswordView.as_view()),
    # 注册用户关注方面的子路由
    path('users/like/<int:pk>/', userinfo.UserLikeView.as_view()),
    # 注册用户个人关注标签自路由
    path('user/label/', userinfo.UserLabelView.as_view())
]

