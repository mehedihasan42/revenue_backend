from google.oauth2.credentials import Credentials
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet,ModelViewSet
from django.shortcuts import redirect
from .models import Song
from .serializers import SongSerializer
from .utils.youtube import extract_video_id
from .services.youtube_auth import get_auth_flow
from .services.youtube_data import get_video_details
from .services.youtube_analytics import get_video_revenue
from rest_framework.permissions import AllowAny


class SongViewSet(ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [AllowAny]


def youtube_login(request):
    flow = get_auth_flow()
    auth_url, state = flow.authorization_url(
        access_type='offline',        # important for refresh token
        include_granted_scopes='true',
        prompt='consent'             # important! forces refresh_token each time
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

    return redirect("http://localhost:5173")


def get_credentials_from_session(request):
    creds = request.session.get('credentials')
    if not creds:
        return None
    return Credentials(**creds)


@api_view(['POST'])
@permission_classes([AllowAny])
def fetch_video_from_url(request):
    credentials = get_credentials_from_session(request)
    if not credentials:
        return Response({'error': 'Not authenticated'}, status=401)

    url = request.data.get('url')
    if not url:
        return Response({'error': 'YouTube URL required'}, status=400)

    video_id = extract_video_id(url)
    if not video_id:
        return Response({'error': 'Invalid YouTube URL'}, status=400)

    title, views = get_video_details(credentials, video_id)
    views_analytics, revenue = get_video_revenue(credentials, video_id)

    song, _ = Song.objects.update_or_create(
        video_id=video_id,
        defaults={
            'url': url,
            'title': title,
            'views': views_analytics or views,
            'revenue': revenue
        }
    )

    return Response({
        'message': 'Video saved successfully',
        'data': SongSerializer(song).data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def check_auth(request):
    if request.session.get('credentials'):
        return Response({'authenticated': True})
    return Response({'authenticated': False})

