from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer
from apps.audit.models import AuditLog


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by('-sent_at')
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    @action(detail=True, methods=['post'], url_path='mark-read')
    def mark_read(self, request, pk=None):
        notification = get_object_or_404(Notification, pk=pk)
        notification.is_read = True
        notification.save(update_fields=['is_read'])
        AuditLog.objects.create(user=request.user, role=(request.user.role.name if request.user.role else ''), action='mark_notification_read', module='notifications', new_value={'notification_id': str(notification.id)})
        return Response({'detail': 'Notification marked as read.'}, status=status.HTTP_200_OK)
