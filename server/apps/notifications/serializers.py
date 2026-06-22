from rest_framework import serializers
from .models import Notification
from apps.users.models import User
from apps.users.serializers import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'
