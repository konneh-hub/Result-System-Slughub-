from rest_framework import serializers
from .models import ReportRequest
from apps.users.serializers import UserSerializer


class ReportRequestSerializer(serializers.ModelSerializer):
    requested_by = UserSerializer(read_only=True)

    class Meta:
        model = ReportRequest
        fields = '__all__'
