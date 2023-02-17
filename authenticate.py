import os
# API Key
os.environ["DEVELOPER_KEY"] = 'AIzaSyCOjk3Drh1S6aYeOWKeYdUAtACFjKUTl8g'
# OATHU2.0
os.environ["OAUTH_CREDENTIAL_PATH"] = "credentials/oauth_credential_test.json"
os.environ["SERVICE_ACCOUNT_PATH"] = "credentials/service_account.json"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getcwd() + os.environ["SERVICE_ACCOUNT_PATH"]
# GCP
os.environ["AUDIO_BUCKET_NAME"] = 'youtube-audio-bucket' 
os.environ["VIDEO_BUCKET_NAME"] = 'youtube-audio-bucket' 
# YouTube Data API
os.environ["YOUTUBE_API_SERVICE_NAME"] = "youtube"
os.environ["YOUTUBE_API_VERSION"] = "v3"

