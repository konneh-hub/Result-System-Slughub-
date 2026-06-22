from rest_framework import routers
from .views import StudentProfileViewSet

router = routers.DefaultRouter()
router.register(r'profiles', StudentProfileViewSet, basename='studentprofile')

urlpatterns = router.urls
