# services/youtube_data.py
from googleapiclient.discovery import build

def get_all_videos(credentials):
    youtube = build('youtube', 'v3', credentials=credentials)

    channel = youtube.channels().list(
        part='contentDetails',
        mine=True
    ).execute()

    uploads_playlist_id = channel['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    videos = []
    request = youtube.playlistItems().list(
        part='snippet',
        playlistId=uploads_playlist_id,
        maxResults=50
    )

    while request:
        response = request.execute()
        videos.extend(response['items'])
        request = youtube.playlistItems().list_next(request, response)

    return videos
