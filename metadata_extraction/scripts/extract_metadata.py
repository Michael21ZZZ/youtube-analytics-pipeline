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
#from get_acc_tag import get_accreditation_tag
from datetime import datetime
import re
import json
from cleantext import clean
import pandas as pd
from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession

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

#get accreditation tag from a single video id
def get_accreditation_tag(videoID, channel_id):
    try:
        search_url = "https://www.youtube.com/watch?v="
        video_url = search_url + videoID
        print("Retrieving accTag for: ", video_url)
        #if the video belongs to a verified channel, return 1
        if (channel_id in acc_channel_list):
            return 1
        #if the video belongs to a non-verified channel, return 0
        if (channel_id in noacc_channel_list):
            return 0
        # init an HTML Session
        session = HTMLSession()
        # get the html content
        response = session.get(video_url)
        response.html.render(scrolldown = 4, sleep=1, timeout=60)
        # create bs object to parse HTML
        soup = bs(response.html.html, "html.parser")
        acc_tag_text = soup.find_all("div", {"class":"content style-scope ytd-info-panel-content-renderer"})
        if(len(acc_tag_text) > 0):
            acc_tag = 1
            acc_channel_list.append(channel_id)
        else:
            acc_tag = 0
            noacc_channel_list.append(channel_id)
    except:
        print('error in extracting accTag')
        acc_tag = 0

    return acc_tag

def metadata_extraction(youtube, keyword, video_id, rank):
    print("extracting the keyword: ", keyword)
    print("extracting the rank: ", rank)
    result = {}
    # make API call to get video and channel information
    try:
        video_response = get_video_details(youtube, id=video_id)
        items = video_response.get("items")[0]
        snippet = items["snippet"]
        video_statistics = items["statistics"]
        content_details = items["contentDetails"]
        channel_id = snippet["channelId"]
        channel_response = get_channel_details(youtube, id=channel_id)   
    except:
        print("Failed to extract the videos! The video id is: ", video_id)
        return
    channel_statistics = channel_response["items"][0]["statistics"]
    duration = isodate.parse_duration(content_details["duration"]).total_seconds()
    result["id"] = items["id"]
    result["title"] = snippet["title"]
    result["views"] = video_statistics["viewCount"]
    result["date_published"] = snippet["publishedAt"][0:10]
    result["description"] = snippet["description"].replace('\n', ' ') #remove new line
    try:
        result["tags"] = snippet['tags']
    except:
        result["tags"] = None
    try: 
        result["comments"]= extract_comments(youtube, part="snippet, replies", videoId = video_id, textFormat='plainText')
    except:
        result["comments"]= 0
    try:
        result["likes"] = video_statistics["likeCount"]
    except:
        result["likes"] = 0
    result["channel_name"] = snippet["channelTitle"]
    result["chanenelID"] = snippet["channelId"]
    result["channel_subscribers"] = channel_statistics["subscriberCount"]
    result["accreditationTag"] = get_accreditation_tag(video_id, channel_id)
    result["duration"] = duration
    result["keyword"] = keyword
    result["rank"] = rank
    result["consine similarity"] = calc_cosine_similarity(str(keyword), result["description"])

    return result


if __name__ == '__main__':
    SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    youtube = youtube_authenticate('./credential_and_key/credential.json')
    videoIDs = pd.read_csv('./temp/sampled_filtered_video_list.csv')
    acc_channel_list = []
    noacc_channel_list = []
    f = open('./temp/final_data.json','w')
    for i in range(videoIDs.shape[0]):
        keyword = videoIDs.loc[i, 'keyword']
        video_id = videoIDs.loc[i, 'id']
        rank = int(videoIDs.loc[i, 'rank'])
        metadata = metadata_extraction(youtube, keyword, video_id, rank)
        f.write(json.dumps(metadata))
        f.write('\n')
    f.close()
    print(acc_channel_list)
    print(noacc_channel_list)



