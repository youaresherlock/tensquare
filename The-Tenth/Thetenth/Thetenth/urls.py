"""Thetenth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # 注册登录注册子应用
    path('', include('apps.users.urls')),
    # 注册文章子应用
    path('', include('apps.article.urls')),
    # 注册活动子应用
    path('', include('apps.activity.urls')),
    # 注册吐槽子应用
    path('', include('apps.talks.urls')),
    # 注册问答子应用
    path('', include('apps.asks.urls')),
    # 注册招聘子应用
    path('', include('apps.recruit.urls')),
    # 注册上传图片子应用
    path('', include('apps.uploadimg.urls')),
]
