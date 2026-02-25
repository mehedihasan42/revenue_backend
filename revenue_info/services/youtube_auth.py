import os
from google_auth_oauthlib.flow import Flow
from django.conf import settings

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

def get_auth_flow():
    client_config = {
        "web": {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }

    return Flow.from_client_config(
        client_config,
       scopes=[
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
    "https://www.googleapis.com/auth/yt-analytics-monetary.readonly",
     ],

        redirect_uri="http://localhost:8000/api/oauth/callback/"
    )
