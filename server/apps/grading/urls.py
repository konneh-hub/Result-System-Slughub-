from rest_framework import routers
from .views import GradingRuleViewSet, GradingSchemeViewSet

router = routers.DefaultRouter()
router.register(r'rules', GradingRuleViewSet, basename='gradingrule')
router.register(r'schemes', GradingSchemeViewSet, basename='gradingscheme')

urlpatterns = router.urls
