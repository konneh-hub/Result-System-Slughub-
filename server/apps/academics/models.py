from django.db import models
from django.utils import timezone
import uuid


class Faculty(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=200, unique=True)
	code = models.CharField(max_length=20, blank=True)
	created_at = models.DateTimeField(default=timezone.now)

	class Meta:
		db_table = 'academics_faculty'
		ordering = ['name']

	def __str__(self):
		return self.name


class Department(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments')
	name = models.CharField(max_length=200)
	code = models.CharField(max_length=20, blank=True)
	created_at = models.DateTimeField(default=timezone.now)

	class Meta:
		db_table = 'academics_department'
		unique_together = ('faculty', 'name')
		ordering = ['name']

	def __str__(self):
		return f"{self.name} ({self.faculty.name})"


class Programme(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='programmes')
	name = models.CharField(max_length=200)
	code = models.CharField(max_length=50, blank=True)
	duration_years = models.PositiveSmallIntegerField(default=3)
	created_at = models.DateTimeField(default=timezone.now)

	class Meta:
		db_table = 'academics_programme'
		ordering = ['name']

	def __str__(self):
		return self.name


class AcademicSession(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=64, unique=True)
	is_active = models.BooleanField(default=False)
	start_date = models.DateField(null=True, blank=True)
	end_date = models.DateField(null=True, blank=True)

	class Meta:
		db_table = 'academics_session'
		ordering = ['-name']

	def __str__(self):
		return self.name


class Semester(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name='semesters')
	name = models.CharField(max_length=64)
	start_date = models.DateField(null=True, blank=True)
	end_date = models.DateField(null=True, blank=True)

	class Meta:
		db_table = 'academics_semester'
		unique_together = ('session', 'name')

	def __str__(self):
		return f"{self.name} - {self.session.name}"
