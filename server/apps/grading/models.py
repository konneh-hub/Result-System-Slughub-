from django.db import models
from django.utils import timezone
import uuid


class GradingRule(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=128)
	min_score = models.DecimalField(max_digits=5, decimal_places=2)
	max_score = models.DecimalField(max_digits=5, decimal_places=2)
	grade = models.CharField(max_length=8)
	point = models.DecimalField(max_digits=4, decimal_places=2)
	created_at = models.DateTimeField(default=timezone.now)

	class Meta:
		db_table = 'grading_rule'
		ordering = ['-point']

	def __str__(self):
		return f"{self.grade} ({self.min_score}-{self.max_score})"


class GradingScheme(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=128)
	created_at = models.DateTimeField(default=timezone.now)
	rules = models.ManyToManyField(GradingRule, related_name='schemes')

	class Meta:
		db_table = 'grading_scheme'

	def __str__(self):
		return self.name
