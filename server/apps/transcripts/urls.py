from rest_framework.routers import DefaultRouter
from .views import TranscriptRequestViewSet

router = DefaultRouter()
router.register(r'transcripts', TranscriptRequestViewSet, basename='transcriptrequest')

urlpatterns = router.urls
