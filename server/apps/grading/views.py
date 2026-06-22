from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import GradingRule, GradingScheme
from .serializers import GradingRuleSerializer, GradingSchemeSerializer


class GradingRuleViewSet(viewsets.ModelViewSet):
	queryset = GradingRule.objects.all().order_by('-min_score')
	serializer_class = GradingRuleSerializer
	permission_classes = [IsAuthenticated]


class GradingSchemeViewSet(viewsets.ModelViewSet):
	queryset = GradingScheme.objects.all().order_by('name')
	serializer_class = GradingSchemeSerializer
	permission_classes = [IsAuthenticated]
