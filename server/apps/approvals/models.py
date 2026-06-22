from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class ApprovalRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='approval_requests')
    approver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approvals_to_review')
    module = models.CharField(max_length=128, blank=True)
    status = models.CharField(max_length=32, default='pending')
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'approvals_request'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.status})"


class ApprovalAction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    approval_request = models.ForeignKey(ApprovalRequest, on_delete=models.CASCADE, related_name='actions')
    approver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    approved = models.BooleanField(default=False)
    comment = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'approvals_action'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.approval_request.title} - {'approved' if self.approved else 'rejected'}"