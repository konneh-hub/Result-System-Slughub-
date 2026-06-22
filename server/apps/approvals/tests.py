from rest_framework.test import APITestCase
from apps.users.models import User
from apps.approvals.models import ApprovalRequest


class ApprovalFlowTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='approver', email='approver@example.com', password='password123')
        self.client.force_authenticate(user=self.user)

    def test_create_approval_request(self):
        payload = {
            'title': 'Approve grade change',
            'description': 'Please review the submitted result entry.',
            'module': 'results',
        }
        response = self.client.post('/api/v1/approval-requests/', payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], payload['title'])
        self.assertEqual(response.data['status'], 'pending')
        self.assertEqual(response.data['requester']['id'], str(self.user.id))

    def test_create_approval_action(self):
        approval_request = ApprovalRequest.objects.create(
            title='Approve transcript',
            description='Transcript generation requires approval.',
            requester=self.user,
            module='transcripts',
        )
        payload = {
            'approval_request': str(approval_request.id),
            'approved': True,
            'comment': 'Approved for publication.',
        }
        response = self.client.post('/api/v1/approval-actions/', payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data['approved'])
        self.assertEqual(str(response.data['approval_request']), str(approval_request.id))
