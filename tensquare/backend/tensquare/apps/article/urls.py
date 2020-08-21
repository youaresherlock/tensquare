from rest_framework.routers import SimpleRouter

from article import views

urlpatterns = [

]
router = SimpleRouter()
router.register(r'article', views.ArticleViewSet)
router.register(r'channels', views.ChannelViewSet)
router.register('articles/search', views.ArticleSearchViewSet, base_name='articles_search')
urlpatterns += router.urls
