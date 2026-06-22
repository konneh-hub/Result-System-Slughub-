from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import StudentProfile
from .serializers import StudentProfileSerializer
from apps.grading.services import compute_cgpa


class StudentProfileViewSet(viewsets.ModelViewSet):
	queryset = StudentProfile.objects.all().order_by('-created_at')
	serializer_class = StudentProfileSerializer
	permission_classes = [IsAuthenticated]

	@action(detail=True, methods=['get'], url_path='cgpa')
	def cgpa(self, request, pk=None):
		student = get_object_or_404(StudentProfile, pk=pk)
		cgpa_value = compute_cgpa(student)
		return Response({'student_id': str(student.id), 'cgpa': cgpa_value})
