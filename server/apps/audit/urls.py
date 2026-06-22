from rest_framework import routers
from .views import AuditLogViewSet

router = routers.DefaultRouter()
router.register(r'audit-logs', AuditLogViewSet, basename='auditlog')
