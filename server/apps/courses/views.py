from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Course, CourseOffering, CourseAssignment
from .serializers import CourseSerializer, CourseOfferingSerializer, CourseAssignmentSerializer

class CourseViewSet(viewsets.ModelViewSet):
	queryset = Course.objects.all().order_by('code')
	serializer_class = CourseSerializer
	permission_classes = [IsAuthenticated]

class CourseOfferingViewSet(viewsets.ModelViewSet):
	queryset = CourseOffering.objects.all().order_by('-created_at')
	serializer_class = CourseOfferingSerializer
	permission_classes = [IsAuthenticated]

class CourseAssignmentViewSet(viewsets.ModelViewSet):
	queryset = CourseAssignment.objects.all().order_by('-assigned_at')
	serializer_class = CourseAssignmentSerializer
	permission_classes = [IsAuthenticated]
