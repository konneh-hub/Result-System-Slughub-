from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings

from apps.users.serializers import LoginSerializer, UserSerializer, ForgotPasswordSerializer, ResetPasswordSerializer, ChangePasswordSerializer
from apps.users.models import User
from apps.audit.models import AuditLog


UserModel = get_user_model()


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        user = None
        if email:
            try:
                user = UserModel.objects.get(email__iexact=email)
                username = user.username
            except UserModel.DoesNotExist:
                pass

        user = authenticate(request, username=username, password=password)

        if not user:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if user.is_locked:
            return Response({'detail': 'Account locked due to failed login attempts'}, status=status.HTTP_403_FORBIDDEN)

        # Reset failed attempts on successful login
        user.failed_login_attempts = 0
        user.save(update_fields=['failed_login_attempts'])

        refresh = RefreshToken.for_user(user)
        data = {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data,
        }

        # Audit log
        AuditLog.objects.create(user=user, role=(user.role.name if user.role else ''), action='login', module='auth', ip_address=self._get_ip(request))

        return Response(data, status=status.HTTP_200_OK)

    def _get_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Blacklist the refresh token
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'detail': 'Refresh token required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        AuditLog.objects.create(user=request.user, role=(request.user.role.name if request.user.role else ''), action='logout', module='auth', ip_address=self._get_ip(request))

        return Response({'detail': 'Logged out'}, status=status.HTTP_200_OK)

    def _get_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class TokenRefreshViewCustom(TokenRefreshView):
    permission_classes = [AllowAny]


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = UserModel.objects.get(email__iexact=email)
        except UserModel.DoesNotExist:
            return Response({'detail': 'If that email exists, password reset instructions were sent.'}, status=status.HTTP_200_OK)

        token = default_token_generator.make_token(user)
        reset_url = f"{request.scheme}://{request.get_host()}/reset-password/?uid={user.pk}&token={token}"
        # send email (console backend used for dev by default)
        send_mail(
            subject='Password reset',
            message=f'Use the following link to reset your password: {reset_url}',
            from_email=settings.EMAIL_FROM,
            recipient_list=[email],
        )

        AuditLog.objects.create(user=user, role=(user.role.name if user.role else ''), action='forgot_password', module='auth', ip_address=self._get_ip(request))

        return Response({'detail': 'If that email exists, password reset instructions were sent.'}, status=status.HTTP_200_OK)

    def _get_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uid = serializer.validated_data.get('uid')
        token = serializer.validated_data.get('token')
        new_password = serializer.validated_data.get('new_password')

        if not uid or not token:
            return Response({'detail': 'UID and token are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserModel.objects.get(pk=uid)
        except UserModel.DoesNotExist:
            return Response({'detail': 'Invalid reset link.'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({'detail': 'Reset token is invalid or expired.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        AuditLog.objects.create(user=user, role=(user.role.name if user.role else ''), action='password_reset', module='auth', ip_address=self._get_ip(request))

        return Response({'detail': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        user = request.user
        if not user.check_password(old_password):
            return Response({'detail': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()

        AuditLog.objects.create(user=user, role=(user.role.name if user.role else ''), action='change_password', module='auth', ip_address=self._get_ip(request))

        return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)

    def _get_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
