from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('file_sharing.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Add a basic response for the root URL
def health_check(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path('', health_check, name='health_check'),
] + urlpatterns

