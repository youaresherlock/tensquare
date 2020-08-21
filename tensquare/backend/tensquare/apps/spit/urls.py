
from rest_framework_mongoengine.routers import SimpleRouter

from spit import views

urlpatterns = [
]
router = SimpleRouter()
router.register(r'spit', views.SpitViewSet)
urlpatterns += router.urls

