from rest_framework.test import APITestCase
from apps.users.models import User
from apps.reports.models import ReportRequest


class ReportFlowTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='reporter', email='reporter@example.com', password='password123')
        self.client.force_authenticate(user=self.user)

    def test_create_report_request(self):
        payload = {
            'title': 'Student performance summary',
            'description': 'Run a performance report for the faculty.',
            'report_type': 'performance',
            'parameters': {'programme_id': None},
        }
        response = self.client.post('/api/v1/reports/', payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], payload['title'])
        self.assertEqual(response.data['status'], 'pending')
        self.assertEqual(response.data['requested_by']['id'], str(self.user.id))

    def test_generate_report(self):
        report_request = ReportRequest.objects.create(
            requested_by=self.user,
            title='Annual results report',
            description='Generate a summary report.',
            report_type='performance',
        )
        response = self.client.post(f"/api/v1/reports/{report_request.id}/generate/", {}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('summary', response.data)
        report_request.refresh_from_db()
        self.assertEqual(report_request.status, 'completed')
