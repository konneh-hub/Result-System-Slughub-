from rest_framework import serializers
from .models import User
from apps.roles.models import Role
from apps.audit.models import AuditLog


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name', 'description')


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id','username','email','first_name','last_name','phone_number','gender','staff_id','student_id','profile_photo','role','is_active','is_locked','failed_login_attempts','last_login','created_at','updated_at')
        read_only_fields = ('id','created_at','updated_at','failed_login_attempts')


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ('id','username','email','password','first_name','last_name','phone_number','gender','staff_id','student_id')

    def validate(self, attrs):
        role = self.context.get('role')
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.UUIDField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','first_name','last_name','phone_number','gender','profile_photo')


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'
