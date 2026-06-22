from django.urls import path, include
from .auth import LoginView, MeView, LogoutView, TokenRefreshViewCustom, ForgotPasswordView, ResetPasswordView, ChangePasswordView

from apps.users.urls import router as users_router
from apps.roles.urls import router as roles_router
from apps.audit.urls import router as audit_router

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),
    path('auth/token/refresh/', TokenRefreshViewCustom.as_view(), name='token_refresh'),
    path('auth/forgot-password/', ForgotPasswordView.as_view(), name='auth-forgot-password'),
    path('auth/reset-password/', ResetPasswordView.as_view(), name='auth-reset-password'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='auth-change-password'),
    path('auth/me/', MeView.as_view(), name='auth-me'),
    path('', include((users_router.urls, 'users'), namespace='users')),
    path('', include((roles_router.urls, 'roles'), namespace='roles')),
    path('', include((audit_router.urls, 'audit'), namespace='audit')),
]
