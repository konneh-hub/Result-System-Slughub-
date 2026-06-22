from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, UserCreateSerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from apps.roles.models import Role
from apps.audit.models import AuditLog


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create']:
            return UserCreateSerializer
        if self.action in ['profile', 'update_profile']:
            return ProfileSerializer
        return UserSerializer

    @action(detail=False, methods=['get'], url_path='profile')
    def profile(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put'], url_path='profile')
    def update_profile(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='activate')
    def activate(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        user.is_active = True
        user.save(update_fields=['is_active'])
        AuditLog.objects.create(user=request.user, role=(request.user.role.name if request.user.role else ''), action='activate_user', module='users')
        return Response({'detail': 'User activated'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='suspend')
    def suspend(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        user.is_active = False
        user.save(update_fields=['is_active'])
        AuditLog.objects.create(user=request.user, role=(request.user.role.name if request.user.role else ''), action='suspend_user', module='users')
        return Response({'detail': 'User suspended'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='assign-role')
    def assign_role(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        role_id = request.data.get('role_id')
        if not role_id:
            return Response({'detail': 'role_id required'}, status=status.HTTP_400_BAD_REQUEST)
        role = get_object_or_404(Role, pk=role_id)
        user.role = role
        user.save(update_fields=['role'])
        AuditLog.objects.create(user=request.user, role=(request.user.role.name if request.user.role else ''), action=f'assign_role_{role.name}', module='users')
        return Response({'detail': 'Role assigned'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='reset-password')
    def reset_password(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        new_password = request.data.get('new_password')
        if not new_password:
            return Response({'detail': 'new_password required'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        AuditLog.objects.create(user=request.user, role=(request.user.role.name if request.user.role else ''), action='reset_password', module='users')
        return Response({'detail': 'Password reset successfully'}, status=status.HTTP_200_OK)
