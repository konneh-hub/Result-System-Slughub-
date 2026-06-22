from rest_framework import serializers
from .models import Course, CourseOffering, CourseAssignment
from apps.academics.serializers import ProgrammeSerializer, SemesterSerializer


class CourseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = '__all__'


class CourseOfferingSerializer(serializers.ModelSerializer):
	course = CourseSerializer(read_only=True)
	programme = ProgrammeSerializer(read_only=True)
	semester = SemesterSerializer(read_only=True)

	class Meta:
		model = CourseOffering
		fields = '__all__'


class CourseAssignmentSerializer(serializers.ModelSerializer):
	offering = CourseOfferingSerializer(read_only=True)

	class Meta:
		model = CourseAssignment
		fields = '__all__'
