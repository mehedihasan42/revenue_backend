from googleapiclient.discovery import build

def get_video_details(credentials, video_id):
    youtube = build('youtube', 'v3', credentials=credentials)

    response = youtube.videos().list(
        part='snippet,statistics',
        id=video_id
    ).execute()

    if not response['items']:
        return None, 0

    item = response['items'][0]
    title = item['snippet']['title']
    views = int(item['statistics'].get('viewCount', 0))

    return title, views
