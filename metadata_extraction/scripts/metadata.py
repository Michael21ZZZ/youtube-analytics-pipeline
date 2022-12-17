'''
Scripts for metadata extraction.
'''
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
from get_acc_tag import get_accreditation_tag
from datetime import datetime
import re
import json
from cleantext import clean
import pandas as pd

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

def get_video_id_by_url(url):
    """
    Return the Video ID from the video `url`
    """
    # split URL parts
    parsed_url = p.urlparse(url)
    # get the video ID by parsing the query of the URL
    video_id = p.parse_qs(parsed_url.query).get("v")
    if video_id:
        return video_id[0]
    else:
        raise Exception(f"Wasn't able to parse video URL: {url}")

def get_video_details(youtube, **kwargs):
    return youtube.videos().list(
        part="id,snippet,contentDetails,statistics",
        **kwargs
    ).execute()

def parse_channel_url(url):
    """
    This function takes channel `url` to check whether it includes a
    channel ID, user ID or channel name
    """
    path = p.urlparse(url).path
    id = path.split("/")[-1]
    if "/c/" in path:
        return "c", id
    elif "/channel/" in path:
        return "channel", id
    elif "/user/" in path:
        return "user", id

def get_channel_id_by_url(youtube, url):
    """
    Returns channel ID of a given `id` and `method`
    - `method` (str): can be 'c', 'channel', 'user'
    - `id` (str): if method is 'c', then `id` is display name
        if method is 'channel', then it's channel id
        if method is 'user', then it's username
    """
    # parse the channel URL
    method, id = parse_channel_url(url)
    if method == "channel":
        # if it's a channel ID, then just return it
        return id
    elif method == "user":
        # if it's a user ID, make a request to get the channel ID
        response = get_channel_details(youtube, forUsername=id)
        items = response.get("items")
        if items:
            channel_id = items[0].get("id")
            return channel_id
    elif method == "c":
        # if it's a channel name, search for the channel using the name
        # may be inaccurate
        response = search(youtube, q=id, maxResults=1)
        items = response.get("items")
        if items:
            channel_id = items[0]["snippet"]["channelId"]
            return channel_id
    raise Exception(f"Cannot find ID:{id} with {method} method")

def get_channel_details(youtube, **kwargs):
    return youtube.channels().list(
        part="statistics,snippet,contentDetails",
        **kwargs
    ).execute()

# function calculating the similarity of keyword with video description
def calc_cosine_similarity(word1, word2):
    # Cosine similarity calculation
    # tokenization
    X_list = word_tokenize(word1) 
    Y_list = word_tokenize(word2)
      
    # sw contains the list of stopwords
    sw = stopwords.words('english') 
    l1 =[];l2 =[]
      
    # remove stop words from the string
    X_set = {w for w in X_list if not w in sw} 
    Y_set = {w for w in Y_list if not w in sw}
      
    # form a set containing keywords of both strings 
    rvector = X_set.union(Y_set) 
    for w in rvector:
        if w in X_set: l1.append(1) # create a vector
        else: l1.append(0)
        if w in Y_set: l2.append(1)
        else: l2.append(0)
    c = 0
      
    # cosine formula 
    for i in range(len(rvector)):
        c+= l1[i]*l2[i]
    if float((sum(l1)*sum(l2))**0.5) == 0:
        return "NA"
    else:
        return c / float((sum(l1)*sum(l2))**0.5)

def extract_comments(youtube, **kwargs):
    comments_response = youtube.commentThreads().list(**kwargs).execute()
    comments_list = []
    while comments_response:
        for item in comments_response['items']:
            # add main comments
            comments_list.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
            # add replies
            try:
                reply_list = item['replies']['comments']
                for reply_thread in reply_list:
                    comments_list.append(reply_thread['snippet']['textDisplay'])
            except:
                pass
        # Check if another page exists
        if 'nextPageToken' in comments_response:
            kwargs['pageToken'] = comments_response['nextPageToken']
            comments_response = youtube.commentThreads().list(**kwargs).execute()
        else:
            break

    comments_str = " ".join(comments_list).strip()
    # remove emoji from contents
    clean_comments = clean(comments_str, no_emoji=True)

    #return clean_comments
    return len(comments_list)

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

def metadata_extraction(youtube, keyword, video_id, rank):
    print("extracting the keyword: ", keyword)
    print("extracting the rank: ", rank)
    result = {}
    # make API call to get video info
    video_response = get_video_details(youtube, id=video_id)    
    items = video_response.get("items")[0]
    # get the snippet, statistics & content details from the video response
    snippet         = items["snippet"]
    video_statistics      = items["statistics"]
    content_details = items["contentDetails"]
    channel_id = snippet["channelId"]
    # get channel info
    channel_response = get_channel_details(youtube, id=channel_id)
    channel_statistics = channel_response["items"][0]["statistics"]

    # filter based on duration and english
    duration = isodate.parse_duration(content_details["duration"]).total_seconds()

    # store features in result
    result["id"] = items["id"]
    result["title"] = snippet["title"]
    result["views"] = video_statistics["viewCount"]
    result["date_published"] = snippet["publishedAt"][0:10]
    result["description"] = snippet["description"].replace('\n', ' ') #remove new line
    try:
        result["tags"] = snippet['tags']
    except:
        result["tags"] = 'NA'
    try: 
        result["comments"]= extract_comments(youtube, part="snippet, replies", videoId = video_id, textFormat='plainText')
    except:
        result["comments"]= 0
    try:
        result["likes"] = video_statistics["likeCount"]
    except:
        result["likes"] = 'NA'

    result["channel"] = {'name': snippet["channelTitle"], 'chanenelID': snippet["channelId"], 'subscribers': channel_statistics["subscriberCount"]}
    result["accreditationTag"] = get_accreditation_tag(video_id)
    result["duration"] = duration
    result["keyword"] = keyword
    result["rank"] = rank
    result["consine similarity"] = calc_cosine_similarity(str(keyword), result["description"])

    return result


if __name__ == '__main__':
    # authenticate to YouTube API
    SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    # youtube = youtube_authenticate('./credential_and_key/new_credential.json')
    youtube = youtube_authenticate('./credential_and_key/credentials.json')
    #youtube = youtube_authenticate('./credential_and_key/credentials_official.json')
    # df = pd.read_csv('./temp/videoIDs_complete.csv')
    # # filter based on language and duration
    # df['Filtered'] = df.apply(lambda row: filter(row.id), axis = 1)
    # df1 = df[df['Filtered'] == True]
    # # sampling from each keyword
    # df2 = df1.groupby('keyword').apply(lambda s: s.sample(min(len(s), 2)))
    # # select the column and save the result
    # videoIDs = df2.loc[:,['keyword','id','rank']]
    # videoIDs.reset_index(drop=True, inplace=True)
    # # save the result
    # videoIDs.to_csv('./temp/filtered.csv', index=False)
    # # load from temp file
    videoIDs = pd.read_csv('./temp/filtered_four_per_keyword.csv')
    # clear current file    
    #f = open('./temp/complete_data.txt','w')
    f = open('./temp/complete_data.txt','a')
    # write metadata into complete_data.txt
    for i in range(videoIDs.shape[0]):
        keyword = videoIDs.loc[i, 'keyword']
        video_id = videoIDs.loc[i, 'id']
        rank = int(videoIDs.loc[i, 'rank'])
        metadata = metadata_extraction(youtube, keyword, video_id, rank)
        f.write(json.dumps(metadata))
        f.write('\n')
    f.close()

# Trial 1: end at "id": "Ud4HuAzHEUc"

