from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, FileViewSet, FileShareViewSet, ShareableLinkViewSet, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'files', FileViewSet)
router.register(r'file-shares', FileShareViewSet)
router.register(r'shareable-links', ShareableLinkViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/register/', UserViewSet.as_view({'post': 'register'}), name='user-register'),
]

