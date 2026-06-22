from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import ApprovalRequest, ApprovalAction
from .serializers import ApprovalRequestSerializer, ApprovalActionSerializer


class ApprovalRequestViewSet(viewsets.ModelViewSet):
    queryset = ApprovalRequest.objects.all().order_by('-created_at')
    serializer_class = ApprovalRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)


class ApprovalActionViewSet(viewsets.ModelViewSet):
    queryset = ApprovalAction.objects.all().order_by('-timestamp')
    serializer_class = ApprovalActionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(approver=self.request.user)
