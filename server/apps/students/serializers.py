from rest_framework import serializers
from .models import StudentProfile
from apps.users.serializers import UserSerializer


class StudentProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer(read_only=True)

	class Meta:
		model = StudentProfile
		fields = '__all__'
