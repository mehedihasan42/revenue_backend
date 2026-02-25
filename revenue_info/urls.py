from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    SongViewSet,
    youtube_login,
    oauth_callback,
    fetch_video_from_url
)

router = DefaultRouter()
router.register(r'songs', SongViewSet, basename='songs')

urlpatterns = [
    path('oauth/login/', youtube_login),
    path('oauth/callback/', oauth_callback),
    path('video/fetch/', fetch_video_from_url),
    # path('video/delete/<int:id>/', SongViewSet),
]

urlpatterns += router.urls
