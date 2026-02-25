from googleapiclient.discovery import build
from datetime import date, timedelta

def get_video_revenue(credentials, video_id):
    analytics = build('youtubeAnalytics', 'v2', credentials=credentials)

    today = date.today()
    yesterday = today - timedelta(days=1)

    start_date = "2000-01-01"
    end_date = yesterday.strftime("%Y-%m-%d")

    response = analytics.reports().query(
        ids='channel==MINE',
        startDate=start_date,
        endDate=end_date,
        metrics='estimatedRevenue,views',
        dimensions='day',   # IMPORTANT CHANGE
        filters=f'video=={video_id}'
    ).execute()

    total_views = 0
    total_revenue = 0.0

    if response.get('rows'):
        for row in response['rows']:
            # row format: [day, revenue, views]
            total_revenue += float(row[1])
            total_views += int(row[2])

    return total_views, round(total_revenue, 2)