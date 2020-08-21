
from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from question import views

urlpatterns = [
]
router = SimpleRouter()
router.register(r'labels', views.LabelsViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'reply', views.ReplyViewSet)
urlpatterns += router.urls