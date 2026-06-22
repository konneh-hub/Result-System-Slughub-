from django.db import models
from django.utils import timezone
import uuid
from django.conf import settings
from apps.academics.models import Programme, Semester


class Course(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	code = models.CharField(max_length=32, unique=True)
	title = models.CharField(max_length=255)
	credit_units = models.DecimalField(max_digits=4, decimal_places=2, default=3.0)
	created_at = models.DateTimeField(default=timezone.now)

	class Meta:
		db_table = 'courses_course'
		ordering = ['code']

	def __str__(self):
		return f"{self.code} - {self.title}"


class CourseOffering(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='offerings')
	programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name='course_offerings')
	semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
	year = models.CharField(max_length=16, blank=True)
	lecturer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_courses')
	created_at = models.DateTimeField(default=timezone.now)

	class Meta:
		db_table = 'courses_offering'
		unique_together = ('course', 'programme', 'semester', 'year')

	def __str__(self):
		return f"{self.course.code} offered to {self.programme.name} - {self.semester.name}"


class CourseAssignment(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE, related_name='assignments')
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	role = models.CharField(max_length=64, blank=True)
	assigned_at = models.DateTimeField(default=timezone.now)

	class Meta:
		db_table = 'courses_assignment'
		unique_together = ('offering', 'user')

	def __str__(self):
		return f"{self.user} -> {self.offering}"
