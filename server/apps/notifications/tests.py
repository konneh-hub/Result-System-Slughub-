from rest_framework.test import APITestCase
from apps.users.models import User
from apps.students.models import StudentProfile
from apps.notifications.models import Notification


class NotificationFlowTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='recipient', email='recipient@example.com', password='password123')
        self.sender = User.objects.create_user(username='sender', email='sender@example.com', password='password123')
        self.student = StudentProfile.objects.create(user=self.user, matric_no='S003')
        self.client.force_authenticate(user=self.user)

    def test_create_notification(self):
        payload = {
            'user': str(self.user.id),
            'title': 'New announcement',
            'message': 'A new result has been published.',
            'category': 'info',
        }
        response = self.client.post('/api/v1/notifications/', payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], payload['title'])
        self.assertEqual(response.data['user']['id'], str(self.user.id))

    def test_mark_notification_read(self):
        notification = Notification.objects.create(
            user=self.user,
            sender=self.sender,
            title='Reminder',
            message='Submit your grades.',
        )
        response = self.client.post(f'/api/v1/notifications/{notification.id}/mark-read/', {}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], 'Notification marked as read.')
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)
