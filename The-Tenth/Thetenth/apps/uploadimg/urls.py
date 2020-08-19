from django.urls import path, include
from . import views

urlpatterns = [
    # 注册上传公共图片的类视图
    path('upload/avatar/', views.UploadPublicView.as_view()),
    # 注册富文本编辑器上传图片的子路由
    path('upload/common/', views.UploadCommonView.as_view())
]