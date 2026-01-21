from google.oauth2.credentials import Credentials
from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Song
from .serializers import SongSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services.youtube_data import get_all_videos
from .services.youtube_analytics import get_video_revenue
from .utils.youtube import extract_video_id
from django.shortcuts import redirect
from .services.youtube_auth import get_auth_flow

# Create your views here.
# views.py


class SongViewSet(ReadOnlyModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


def save_song(video_id, title, views, revenue):
    Song.objects.update_or_create(
        video_id=video_id,
        defaults={
            'title': title,
            'views': views,
            'revenue': revenue
        }
    )


def youtube_login(request):
    flow = get_auth_flow()
    auth_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    request.session['state'] = state
    return redirect(auth_url)



def oauth_callback(request):
    flow = get_auth_flow()
    flow.fetch_token(authorization_response=request.build_absolute_uri())

    credentials = flow.credentials
    request.session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
    }

    return redirect('/dashboard/')

def get_credentials_from_session(request):
    creds = request.session.get('credentials')
    if not creds:
        return None

    return Credentials(**creds)


@api_view(['POST'])
def fetch_and_save_all_videos(request):
    credentials = get_credentials_from_session(request)
    if not credentials:
        return Response({'error': 'Not authenticated'}, status=401)

    videos = get_all_videos(credentials)

    saved = 0
    for v in videos:
        video_id = v['snippet']['resourceId']['videoId']
        title = v['snippet']['title']

        views, revenue = get_video_revenue(credentials, video_id)

        Song.objects.update_or_create(
            video_id=video_id,
            defaults={
                'title': title,
                'views': views,
                'revenue': revenue
            }
        )
        saved += 1

    return Response({'message': f'{saved} videos saved'})



@api_view(['POST'])
def save_song_api(request):
    serializer = SongSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Saved successfully'})
    return Response(serializer.errors, status=400)
