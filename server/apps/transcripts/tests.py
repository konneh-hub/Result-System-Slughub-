from rest_framework.test import APITestCase
from apps.users.models import User
from apps.students.models import StudentProfile
from apps.transcripts.models import TranscriptRequest


class TranscriptFlowTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='student', email='student@example.com', password='password123')
        self.student = StudentProfile.objects.create(user=self.user, matric_no='S002')
        self.client.force_authenticate(user=self.user)

    def test_request_transcript(self):
        payload = {'student_id': str(self.student.id)}
        response = self.client.post('/api/v1/transcripts/', payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['student']['id'], str(self.student.id))
        self.assertEqual(response.data['status'], 'pending')

    def test_generate_transcript(self):
        transcript_request = TranscriptRequest.objects.create(student=self.student, requested_by=self.user)
        response = self.client.post(f"/api/v1/transcripts/{transcript_request.id}/generate/", {}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('student', response.data)
        transcript_request.refresh_from_db()
        self.assertEqual(transcript_request.status, 'completed')
