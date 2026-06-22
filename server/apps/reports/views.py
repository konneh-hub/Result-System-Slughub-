from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import ReportRequest
from .serializers import ReportRequestSerializer
from .services import build_student_performance_report
from apps.audit.models import AuditLog


class ReportRequestViewSet(viewsets.ModelViewSet):
    queryset = ReportRequest.objects.all().order_by('-created_at')
    serializer_class = ReportRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(requested_by=self.request.user)

    @action(detail=True, methods=['post'], url_path='generate')
    def generate(self, request, pk=None):
        report_request = get_object_or_404(ReportRequest, pk=pk)
        payload = build_student_performance_report(report_request)
        AuditLog.objects.create(user=request.user, role=(request.user.role.name if request.user.role else ''), action='generate_report', module='reports', new_value={'report_id': str(report_request.id)})
        return Response(payload)
