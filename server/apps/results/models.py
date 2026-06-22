from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class ResultEntry(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE, related_name='results')
	offering = models.ForeignKey('courses.CourseOffering', on_delete=models.CASCADE, related_name='results')
	ca_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	exam_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	total_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	grade = models.CharField(max_length=8, blank=True)
	grade_point = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
	is_submitted = models.BooleanField(default=False)
	submitted_at = models.DateTimeField(null=True, blank=True)
	is_published = models.BooleanField(default=False)
	published_at = models.DateTimeField(null=True, blank=True)
	published_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='published_results')
	created_at = models.DateTimeField(default=timezone.now)

	class Meta:
		db_table = 'results_entry'
		unique_together = ('student', 'offering')

	def __str__(self):
		return f"{self.student} - {self.offering} -> {self.grade}"


class ResultApproval(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	result = models.ForeignKey(ResultEntry, on_delete=models.CASCADE, related_name='approvals')
	approver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
	role = models.CharField(max_length=64, blank=True)
	approved = models.BooleanField(default=False)
	timestamp = models.DateTimeField(default=timezone.now)

	class Meta:
		db_table = 'results_approval'

	def __str__(self):
		return f"Approval {self.approved} by {self.approver} for {self.result}"
