from django.conf.urls import url

from gathering import views

urlpatterns = [
    url(r"^gatherings/$", views.GathersView.as_view()),
    url(r"^gatherings/(?P<pk>[^/.]+)/$", views.GatherView.as_view()),
    url(r"^gatherings/(?P<pk>[^/.]+)/join/$", views.GatherJoinView.as_view()),
]

