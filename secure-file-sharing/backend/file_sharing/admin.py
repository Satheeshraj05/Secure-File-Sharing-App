from django.contrib import admin
from .models import File, FileShare, ShareableLink, MFADevice

admin.site.register(File)
admin.site.register(FileShare)
admin.site.register(ShareableLink)
admin.site.register(MFADevice)

