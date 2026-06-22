from rest_framework.test import APITestCase
from apps.users.models import User
from apps.students.models import StudentProfile


class ComplaintFlowTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='student', email='student@example.com', password='password123')
        self.student = StudentProfile.objects.create(user=self.user, matric_no='S001')
        self.client.force_authenticate(user=self.user)

    def test_create_complaint(self):
        payload = {
            'student_id': str(self.student.id),
            'title': 'Missing grade',
            'description': 'My grade was not posted for the semester.',
            'category': 'results',
        }
        response = self.client.post('/api/v1/complaints/', payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], payload['title'])
        self.assertEqual(response.data['status'], 'open')
        self.assertEqual(response.data['student']['id'], str(self.student.id))

    def test_resolve_complaint(self):
        complaint = self.client.post('/api/v1/complaints/', {
            'student_id': str(self.student.id),
            'title': 'Score discrepancy',
            'description': 'My exam score does not match.',
            'category': 'results',
        }, format='json').data
        response = self.client.post(f"/api/v1/complaints/{complaint['id']}/resolve/", {
            'response': 'The discrepancy has been corrected.',
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], 'Complaint marked resolved.')
