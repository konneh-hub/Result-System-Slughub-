from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ResultEntry, ResultApproval
from .serializers import ResultEntrySerializer, ResultApprovalSerializer
from apps.audit.models import AuditLog
from apps.grading.services import compute_result_entry_grade


class ResultEntryViewSet(viewsets.ModelViewSet):
	queryset = ResultEntry.objects.all().order_by('-created_at')
	serializer_class = ResultEntrySerializer
	permission_classes = [IsAuthenticated]

	@action(detail=True, methods=['post'], url_path='submit')
	def submit(self, request, pk=None):
		result = get_object_or_404(ResultEntry, pk=pk)
		result.is_submitted = True
		result.submitted_at = result.submitted_at or timezone.now()
		result.save(update_fields=['is_submitted', 'submitted_at'])
		AuditLog.objects.create(user=request.user, role=(request.user.role.name if request.user.role else ''), action='submit_result', module='results')
		return Response({'detail': 'Result submitted for review.'}, status=status.HTTP_200_OK)

	@action(detail=True, methods=['post'], url_path='compute-grade')
	def compute_grade(self, request, pk=None):
		result = get_object_or_404(ResultEntry, pk=pk)
		total, grade, point = compute_result_entry_grade(result)
		if grade is None:
			return Response({'detail': 'Cannot compute grade without CA and exam scores.'}, status=status.HTTP_400_BAD_REQUEST)
		result.total_score = total
		result.grade = grade
		result.grade_point = point
		result.save(update_fields=['total_score', 'grade', 'grade_point'])
		AuditLog.objects.create(user=request.user, role=(request.user.role.name if request.user.role else ''), action='compute_grade', module='results', new_value={'grade': grade, 'grade_point': point})
		serializer = self.get_serializer(result)
		return Response(serializer.data)

	@action(detail=True, methods=['post'], url_path='publish')
	def publish(self, request, pk=None):
		result = get_object_or_404(ResultEntry, pk=pk)
		result.is_published = True
		result.published_at = result.published_at or timezone.now()
		result.published_by = request.user
		result.save(update_fields=['is_published', 'published_at', 'published_by'])
		AuditLog.objects.create(user=request.user, role=(request.user.role.name if request.user.role else ''), action='publish_result', module='results')
		return Response({'detail': 'Result published.'}, status=status.HTTP_200_OK)


class ResultApprovalViewSet(viewsets.ModelViewSet):
	queryset = ResultApproval.objects.all().order_by('-timestamp')
	serializer_class = ResultApprovalSerializer
	permission_classes = [IsAuthenticated]

	@action(detail=True, methods=['post'], url_path='approve')
	def approve(self, request, pk=None):
		approval = get_object_or_404(ResultApproval, pk=pk)
		approval.approved = True
		approval.comment = request.data.get('comment', approval.comment)
		approval.approver = request.user
		approval.save(update_fields=['approved', 'comment', 'approver'])
		AuditLog.objects.create(user=request.user, role=(request.user.role.name if request.user.role else ''), action='approve_result', module='results')
		return Response({'detail': 'Approval recorded.'}, status=status.HTTP_200_OK)

	@action(detail=True, methods=['post'], url_path='reject')
	def reject(self, request, pk=None):
		approval = get_object_or_404(ResultApproval, pk=pk)
		approval.approved = False
		approval.comment = request.data.get('comment', approval.comment)
		approval.approver = request.user
		approval.save(update_fields=['approved', 'comment', 'approver'])
		AuditLog.objects.create(user=request.user, role=(request.user.role.name if request.user.role else ''), action='reject_result', module='results')
		return Response({'detail': 'Rejection recorded.'}, status=status.HTTP_200_OK)
