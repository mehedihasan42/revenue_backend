# services/youtube_analytics.py
from googleapiclient.discovery import build
from datetime import date

def get_video_revenue(credentials, video_id):
    analytics = build('youtubeAnalytics', 'v2', credentials=credentials)

    response = analytics.reports().query(
        ids='channel==MINE',
        startDate='2023-01-01',
        endDate=date.today().isoformat(),
        metrics='estimatedRevenue,views',
        dimensions='video',
        filters=f'video=={video_id}'
    ).execute()

    if response.get('rows'):
        views, revenue = response['rows'][0][1:]
        return int(views), float(revenue)

    return 0, 0
