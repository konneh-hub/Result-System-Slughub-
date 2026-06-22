from rest_framework import serializers
from .models import Faculty, Department, Programme, AcademicSession, Semester


class FacultySerializer(serializers.ModelSerializer):
	class Meta:
		model = Faculty
		fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
	faculty = FacultySerializer(read_only=True)

	class Meta:
		model = Department
		fields = '__all__'


class ProgrammeSerializer(serializers.ModelSerializer):
	department = DepartmentSerializer(read_only=True)

	class Meta:
		model = Programme
		fields = '__all__'


class AcademicSessionSerializer(serializers.ModelSerializer):
	class Meta:
		model = AcademicSession
		fields = '__all__'


class SemesterSerializer(serializers.ModelSerializer):
	session = AcademicSessionSerializer(read_only=True)

	class Meta:
		model = Semester
		fields = '__all__'
