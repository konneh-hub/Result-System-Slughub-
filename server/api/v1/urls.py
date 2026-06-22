from django.urls import path, include
from .auth import LoginView, MeView, LogoutView, TokenRefreshViewCustom, ForgotPasswordView, ResetPasswordView, ChangePasswordView

from apps.users.urls import router as users_router
from apps.roles.urls import router as roles_router
from apps.audit.urls import router as audit_router
from apps.academics.urls import router as academics_router
from apps.courses.urls import router as courses_router
from apps.students.urls import router as students_router
from apps.grading.urls import router as grading_router
from apps.results.urls import router as results_router
from apps.approvals.urls import router as approvals_router
from apps.complaints.urls import router as complaints_router
from apps.notifications.urls import router as notifications_router
from apps.reports.urls import router as reports_router
from apps.transcripts.urls import router as transcripts_router

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
    path('', include((academics_router.urls, 'academics'), namespace='academics')),
    path('', include((courses_router.urls, 'courses'), namespace='courses')),
    path('', include((students_router.urls, 'students'), namespace='students')),
    path('', include((grading_router.urls, 'grading'), namespace='grading')),
    path('', include((results_router.urls, 'results'), namespace='results')),
    path('', include((approvals_router.urls, 'approvals'), namespace='approvals')),
    path('', include((complaints_router.urls, 'complaints'), namespace='complaints')),
    path('', include((notifications_router.urls, 'notifications'), namespace='notifications')),
    path('', include((reports_router.urls, 'reports'), namespace='reports')),
    path('', include((transcripts_router.urls, 'transcripts'), namespace='transcripts')),
]
