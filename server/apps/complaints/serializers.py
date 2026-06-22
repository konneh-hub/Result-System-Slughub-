from rest_framework import serializers
from apps.students.models import StudentProfile
from .models import Complaint
from apps.students.serializers import StudentProfileSerializer
from apps.users.serializers import UserSerializer


class ComplaintSerializer(serializers.ModelSerializer):
    student = StudentProfileSerializer(read_only=True)
    raised_by = UserSerializer(read_only=True)
    resolved_by = UserSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(queryset=StudentProfile.objects.all(), source='student', write_only=True)

    class Meta:
        model = Complaint
        fields = '__all__'
