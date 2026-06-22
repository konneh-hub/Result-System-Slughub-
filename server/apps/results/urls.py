from rest_framework import routers
from .views import ResultEntryViewSet, ResultApprovalViewSet

router = routers.DefaultRouter()
router.register(r'entries', ResultEntryViewSet, basename='resultentry')
router.register(r'approvals', ResultApprovalViewSet, basename='resultapproval')

urlpatterns = router.urls
