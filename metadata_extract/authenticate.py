import os

# API Key
os.environ["DEVELOPER_KEY"] = 'AIzaSyCOjk3Drh1S6aYeOWKeYdUAtACFjKUTl8g'
# OATHU2.0
os.environ["OAUTH_CREDENTIAL"] = str({"installed":{"client_id":"45152107222-al8csdiq5n470pknclhuv4a57gjr6h6r.apps.googleusercontent.com","project_id":"geometric-rock-358702","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"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","redirect_uris":["http://localhost"]}})
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
# GCP
os.environ["AUDIO_BUCKET_NAME"] = 'youtube-audio-bucket' 
os.environ["VIDEO_BUCKET_NAME"] = 'youtube-audio-bucket' 
# YouTube Data API
os.environ["YOUTUBE_API_SERVICE_NAME"] = "youtube"
os.environ["YOUTUBE_API_VERSION"] = "v3"

