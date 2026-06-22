from rest_framework import serializers
from .models import TranscriptRequest
from apps.students.serializers import StudentProfileSerializer


class TranscriptRequestSerializer(serializers.ModelSerializer):
    student = StudentProfileSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(queryset=StudentProfileSerializer.Meta.model.objects.all(), source='student', write_only=True)

    class Meta:
        model = TranscriptRequest
        fields = '__all__'
