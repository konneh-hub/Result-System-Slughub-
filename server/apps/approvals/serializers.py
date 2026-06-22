from rest_framework import serializers
from .models import ApprovalRequest, ApprovalAction
from apps.results.models import ResultEntry
from apps.students.serializers import StudentProfileSerializer
from apps.users.serializers import UserSerializer
from apps.courses.serializers import CourseOfferingSerializer


class ApprovalActionSerializer(serializers.ModelSerializer):
    approver = UserSerializer(read_only=True)

    class Meta:
        model = ApprovalAction
        fields = '__all__'


class ApprovalRequestSerializer(serializers.ModelSerializer):
    requester = UserSerializer(read_only=True)
    approver = UserSerializer(read_only=True)
    actions = ApprovalActionSerializer(many=True, read_only=True)

    class Meta:
        model = ApprovalRequest
        fields = '__all__'
