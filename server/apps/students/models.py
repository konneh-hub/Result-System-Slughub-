from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class StudentProfile(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
	matric_no = models.CharField(max_length=64, unique=True, null=True, blank=True)
	programme = models.ForeignKey('academics.Programme', on_delete=models.SET_NULL, null=True, blank=True)
	year_of_admission = models.CharField(max_length=10, blank=True)
	created_at = models.DateTimeField(default=timezone.now)

	class Meta:
		db_table = 'students_profile'
		ordering = ['matric_no']

	def __str__(self):
		return f"{self.user.username} ({self.matric_no})"
