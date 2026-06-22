from rest_framework import routers
from .views import CourseViewSet, CourseOfferingViewSet, CourseAssignmentViewSet

router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'offerings', CourseOfferingViewSet, basename='offering')
router.register(r'assignments', CourseAssignmentViewSet, basename='assignment')

urlpatterns = router.urls
