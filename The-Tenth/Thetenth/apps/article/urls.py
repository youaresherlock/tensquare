from . import views
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter


urlpatterns = [
    path('channels/', views.ChannelsView.as_view()),
]
router = SimpleRouter()
router.register('article', views.ArticleViewSet, basename='article')
router.register('articles/search', views.ArticleSearchViewSet, basename='articles_search')

urlpatterns += router.urls





























