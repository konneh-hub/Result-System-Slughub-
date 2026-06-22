from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import User
from apps.audit.models import AuditLog


@receiver(post_save, sender=User)
def user_saved(sender, instance, created, **kwargs):
    action = 'created' if created else 'updated'
    AuditLog.objects.create(user=instance, role=(instance.role.name if instance.role else ''), action=f'user_{action}', module='users')


@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    AuditLog.objects.create(user=user, role=(user.role.name if user.role else ''), action='login', module='auth', ip_address=request.META.get('REMOTE_ADDR', ''))


@receiver(user_logged_out)
def on_user_logged_out(sender, request, user, **kwargs):
    AuditLog.objects.create(user=user, role=(user.role.name if user and user.role else ''), action='logout', module='auth', ip_address=request.META.get('REMOTE_ADDR', ''))
