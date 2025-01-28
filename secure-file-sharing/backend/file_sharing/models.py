from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

class File(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.CharField(max_length=255)  # Changed from FileField to CharField
    name = models.CharField(max_length=255)
    encrypted_key = models.TextField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class FileShare(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.CharField(max_length=10, choices=[('view', 'View'), ('download', 'Download')])
    expiration = models.DateTimeField()

class ShareableLink(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    expiration = models.DateTimeField()

class MFADevice(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    secret_key = models.CharField(max_length=32)

