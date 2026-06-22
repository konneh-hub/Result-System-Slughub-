from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Complaint
from .serializers import ComplaintSerializer
from apps.audit.models import AuditLog


class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all().order_by('-created_at')
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(raised_by=self.request.user)

    @action(detail=True, methods=['post'], url_path='resolve')
    def resolve(self, request, pk=None):
        complaint = get_object_or_404(Complaint, pk=pk)
        complaint.status = 'resolved'
        complaint.response = request.data.get('response', complaint.response)
        complaint.resolved_by = request.user
        complaint.resolved_at = timezone.now()
        complaint.save(update_fields=['status', 'response', 'resolved_by', 'resolved_at'])
        AuditLog.objects.create(user=request.user, role=(request.user.role.name if request.user.role else ''), action='resolve_complaint', module='complaints', new_value={'status': complaint.status})
        return Response({'detail': 'Complaint marked resolved.'}, status=status.HTTP_200_OK)
