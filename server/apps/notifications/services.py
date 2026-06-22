from apps.notifications.models import Notification
from django.utils import timezone


def send_notification(user, sender, title, message, category='info', data=None):
    return Notification.objects.create(
        user=user,
        sender=sender,
        title=title,
        message=message,
        category=category,
        data=data or {},
        sent_at=timezone.now(),
    )
