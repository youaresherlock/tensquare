
from django.conf.urls import url

from upload import viewsForQiniu
from upload import views

urlpatterns = [
    # url(r'^upload/common/$', viewsForQiniu.ImageUploadViewForCKEditor.as_view()),
    # url(r'^upload/avatar/$', viewsForQiniu.ImageUploadViewForAvatar.as_view()),
    url(r'^upload/common/$', views.ImageUploadViewForCKEditor.as_view()),
    url(r'^upload/avatar/$', views.ImageUploadViewForAvatar.as_view()),
]
