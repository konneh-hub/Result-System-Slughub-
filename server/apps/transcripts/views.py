from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import TranscriptRequest
from .serializers import TranscriptRequestSerializer
from .services import build_transcript_payload
from apps.audit.models import AuditLog


class TranscriptRequestViewSet(viewsets.ModelViewSet):
    queryset = TranscriptRequest.objects.all().order_by('-created_at')
    serializer_class = TranscriptRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(requested_by=self.request.user)

    @action(detail=True, methods=['post'], url_path='generate')
    def generate(self, request, pk=None):
        transcript_request = get_object_or_404(TranscriptRequest, pk=pk)
        payload = build_transcript_payload(transcript_request)
        AuditLog.objects.create(user=request.user, role=(request.user.role.name if request.user.role else ''), action='generate_transcript', module='transcripts', new_value={'request_id': str(transcript_request.id)})
        return Response(payload)
