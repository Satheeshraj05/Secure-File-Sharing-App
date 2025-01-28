# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import File, FileShare, ShareableLink, MFADevice

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'file', 'name', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at', 'file', 'name']

class FileShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileShare
        fields = ['id', 'file', 'shared_with', 'permission', 'expiration']

class ShareableLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareableLink
        fields = ['id', 'file', 'token', 'expiration']
        read_only_fields = ['token']

class MFADeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MFADevice
        fields = ['id', 'user', 'secret_key']
        read_only_fields = ['secret_key']
