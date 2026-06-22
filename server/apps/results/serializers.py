from rest_framework import serializers
from .models import ResultEntry, ResultApproval
from apps.students.models import StudentProfile
from apps.students.serializers import StudentProfileSerializer
from apps.courses.models import CourseOffering
from apps.courses.serializers import CourseOfferingSerializer


class ResultEntrySerializer(serializers.ModelSerializer):
	student = StudentProfileSerializer(read_only=True)
	offering = CourseOfferingSerializer(read_only=True)
	student_id = serializers.PrimaryKeyRelatedField(queryset=StudentProfile.objects.all(), source='student', write_only=True)
	offering_id = serializers.PrimaryKeyRelatedField(queryset=CourseOffering.objects.all(), source='offering', write_only=True)

	class Meta:
		model = ResultEntry
		fields = '__all__'


class ResultApprovalSerializer(serializers.ModelSerializer):
	result = ResultEntrySerializer(read_only=True)
	result_id = serializers.PrimaryKeyRelatedField(queryset=ResultEntry.objects.all(), source='result', write_only=True)

	class Meta:
		model = ResultApproval
		fields = '__all__'
