from rest_framework.routers import DefaultRouter
from .views import ApprovalRequestViewSet, ApprovalActionViewSet

router = DefaultRouter()
router.register(r'approval-requests', ApprovalRequestViewSet, basename='approvalrequest')
router.register(r'approval-actions', ApprovalActionViewSet, basename='approvalaction')

urlpatterns = router.urls
