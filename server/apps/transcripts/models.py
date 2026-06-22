from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class TranscriptRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE, related_name='transcript_requests')
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='requested_transcripts')
    status = models.CharField(max_length=32, default='pending')
    generated_at = models.DateTimeField(null=True, blank=True)
    payload = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'transcripts_request'
        ordering = ['-created_at']

    def __str__(self):
        return f"Transcript request for {self.student} ({self.status})"
