

from recruit import views
from rest_framework.routers import SimpleRouter
urlpatterns = []

router = SimpleRouter()
router.register(r'enterprise', views.EnterpriseViewSet)
router.register(r'recruits', views.RecruitViewSet)
router.register(r'city', views.CityViewSet)
urlpatterns += router.urls