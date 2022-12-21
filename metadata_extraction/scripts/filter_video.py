from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import urllib.parse as p
import re
import os
import sys
import pickle
import isodate
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
#from get_acc_tag import get_accreditation_tag
from datetime import datetime

def youtube_authenticate(client_secrets_file):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build(api_service_name, api_version, credentials=creds)

def get_video_details(youtube, **kwargs):
    return youtube.videos().list(
        part="id,snippet,contentDetails,statistics",
        **kwargs
    ).execute()

# filter based on duration and default language
def filter(video_id):
    try:
        #print("trying ", video_id)
        video_response = get_video_details(youtube, id=video_id)
        items = video_response.get("items")[0]
        content_details = items["contentDetails"]
        snippet         = items["snippet"]
        duration = isodate.parse_duration(content_details["duration"]).total_seconds()
        try:
            default_language = snippet["defaultLanguage"]
        except:
            default_language = 'en'
        flag = (duration < 361) and (duration >= 59) and (default_language == 'en')
    except:
        #print(video_id, " not working")
        flag = False

    return flag

if __name__ == '__main__':
    SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    youtube = youtube_authenticate('./credential_and_key/credential.json')
    complete_videos = pd.read_csv('./temp/videoID_list.csv')
    complete_videos['toKeep'] = complete_videos.apply(lambda x: filter(x['id']), axis = 1)
    filtered_videos = complete_videos[complete_videos['toKeep'] == True]
    sampled_videos = filtered_videos.groupby('keyword').apply(lambda s: s.sample(min(len(s), 4)))
    sampled_videos = sampled_videos.loc[:,['keyword','id','rank']]
    sampled_videos.to_csv('./temp/sampled_filtered_video_list.csv', index = False)

    