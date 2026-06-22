from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Faculty, Department, Programme, AcademicSession, Semester
from .serializers import FacultySerializer, DepartmentSerializer, ProgrammeSerializer, AcademicSessionSerializer, SemesterSerializer


class FacultyViewSet(viewsets.ModelViewSet):
	queryset = Faculty.objects.all().order_by('name')
	serializer_class = FacultySerializer
	permission_classes = [IsAuthenticated]


class DepartmentViewSet(viewsets.ModelViewSet):
	queryset = Department.objects.all().order_by('name')
	serializer_class = DepartmentSerializer
	permission_classes = [IsAuthenticated]


class ProgrammeViewSet(viewsets.ModelViewSet):
	queryset = Programme.objects.all().order_by('name')
	serializer_class = ProgrammeSerializer
	permission_classes = [IsAuthenticated]


class AcademicSessionViewSet(viewsets.ModelViewSet):
	queryset = AcademicSession.objects.all().order_by('-name')
	serializer_class = AcademicSessionSerializer
	permission_classes = [IsAuthenticated]


class SemesterViewSet(viewsets.ModelViewSet):
	queryset = Semester.objects.all().order_by('name')
	serializer_class = SemesterSerializer
	permission_classes = [IsAuthenticated]
