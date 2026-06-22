from rest_framework import serializers
from .models import GradingRule, GradingScheme


class GradingRuleSerializer(serializers.ModelSerializer):
	class Meta:
		model = GradingRule
		fields = '__all__'


class GradingSchemeSerializer(serializers.ModelSerializer):
	rules = GradingRuleSerializer(many=True, read_only=True)

	class Meta:
		model = GradingScheme
		fields = '__all__'
