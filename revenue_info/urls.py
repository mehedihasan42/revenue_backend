# urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    SongViewSet,
    youtube_login,
    oauth_callback,
    fetch_and_save_all_videos,
    save_song_api
)

router = DefaultRouter()
router.register(r'songs', SongViewSet, basename='songs')

urlpatterns = [
    # OAuth
    path('oauth/login/', youtube_login, name='youtube-login'),
    path('oauth/callback/', oauth_callback, name='oauth-callback'),

    # Custom APIs
    path('save-song/', fetch_and_save_all_videos, name='fetch_and_save_all_videos-song'),
    path('save-song/', save_song_api, name='save-song'),
]

# Include router URLs
urlpatterns += router.urls
