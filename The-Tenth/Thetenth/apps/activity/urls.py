from apps.activity import views
from django.urls import re_path

urlpatterns = [
    re_path(r'^gatherings/$', views.GatheringListView.as_view()),
    re_path(r'^gatherings/(?P<pk>\d+)/$', views.GatherView.as_view()),
    re_path(r'^gatherings/(?P<pk>\d+)/join/$', views.GatherJoinView.as_view()),
]