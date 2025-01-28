import os
import logging
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from django.conf import settings
from .models import File, FileShare, ShareableLink, MFADevice
from .serializers import (
    UserSerializer,
    FileSerializer,
    FileShareSerializer,
    ShareableLinkSerializer,
    MFADeviceSerializer,
)
from cryptography.fernet import Fernet, InvalidToken
import pyotp
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse
from rest_framework.renderers import BaseRenderer
import mimetypes

# Setup logger
logger = logging.getLogger(__name__)

# -------------------- Custom Renderer --------------------

class BinaryFileRenderer(BaseRenderer):
    media_type = 'application/octet-stream'
    format = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data

# -------------------- User Management Views --------------------

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling user registration and management.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        """
        Handles user registration.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])  # Set password securely
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT authentication view to include MFA setup.
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = User.objects.get(username=request.data['username'])
            refresh = RefreshToken.for_user(user)
            response.data['refresh'] = str(refresh)
            response.data['access'] = str(refresh.access_token)

            # MFA setup
            mfa_device, created = MFADevice.objects.get_or_create(user=user)
            if created:
                mfa_device.secret_key = pyotp.random_base32()
                mfa_device.save()
            response.data['requires_mfa'] = True
            response.data['mfa_secret'] = mfa_device.secret_key
        return response

# -------------------- File Management Views --------------------

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return File.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({"file": "No file was submitted."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Read file content as bytes
            file_content = file.read()
            
            # Generate encryption key and encrypt
            key = Fernet.generate_key()
            fernet = Fernet(key)
            encrypted_content = fernet.encrypt(file_content)

            # Save encrypted file
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)

            encrypted_file_name = f'encrypted_{file.name}'
            relative_path = f'uploads/{encrypted_file_name}'
            full_path = os.path.join(upload_dir, encrypted_file_name)

            # Write encrypted content
            with open(full_path, 'wb') as f:
                f.write(encrypted_content)

            # Create file instance directly
            file_instance = File.objects.create(
                owner=request.user,
                file=relative_path,
                name=file.name,
                encrypted_key=key.decode()
            )

            serializer = self.get_serializer(file_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Error during file upload: {str(e)}")
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['get'], renderer_classes=[BinaryFileRenderer])
    def download(self, request, pk=None):
        """
        Handles file decryption and download.
        """
        try:
            file = self.get_object()
            
            # Check file existence
            file_path = os.path.join(settings.MEDIA_ROOT, str(file.file))
            if not os.path.exists(file_path):
                return Response(
                    {'error': 'File not found on server.'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            try:
                # Read encrypted content
                with open(file_path, 'rb') as f:
                    encrypted_content = f.read()

                # Decrypt the content
                fernet = Fernet(file.encrypted_key.encode())
                decrypted_content = fernet.decrypt(encrypted_content)

                # Create the response with proper headers
                response = HttpResponse(
                    decrypted_content,
                    content_type='application/octet-stream'
                )
                response['Content-Disposition'] = f'attachment; filename="{file.name}"'
                response['Access-Control-Expose-Headers'] = 'Content-Disposition'
                return response

            except InvalidToken:
                return Response(
                    {'error': 'Unable to decrypt file. The encryption key may be invalid.'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                logger.error(f"Error during file download: {str(e)}")
                return Response(
                    {'error': f'Error processing file: {str(e)}'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        except Exception as e:
            logger.error(f"Error during file download: {str(e)}")
            return Response(
                {'error': f'Error downloading file: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# -------------------- File Sharing Views --------------------

class FileShareViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing file shares between users.
    """
    queryset = FileShare.objects.all()
    serializer_class = FileShareSerializer
    permission_classes = [IsAuthenticated]


class ShareableLinkViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling shareable links for file access.
    """
    queryset = ShareableLink.objects.all()
    serializer_class = ShareableLinkSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def access(self, request, pk=None):
        """
        Allows file access via shareable links.
        """
        link = self.get_object()
        if link.expiration < timezone.now():
            return Response({'error': 'Link has expired'}, status=status.HTTP_400_BAD_REQUEST)

        file = link.file
        file_path = os.path.join(settings.MEDIA_ROOT, file.file.name)
        if not os.path.exists(file_path):
            return Response({'error': 'File not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            with open(file_path, 'rb') as f:
                encrypted_content = f.read()
            fernet = Fernet(file.encrypted_key.encode())
            decrypted_content = fernet.decrypt(encrypted_content)

            response = Response(decrypted_content, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{file.name}"'
            return response
        except InvalidToken:
            return Response({'error': 'Unable to decrypt file. The encryption key may be invalid.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error during file download: {str(e)}")
            return Response({'error': f'An error occurred during file download: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
