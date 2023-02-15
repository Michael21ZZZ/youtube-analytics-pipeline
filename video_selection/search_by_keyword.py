'''
Get video id based on keywords.
Scripts to search videos according to keywords and return video id
Notes:
    1. Update the Developer Key variable with your own key. You can find it here:
    https://cloud.google.com/docs/authentication/api-keys

'''

import sys
import json
import urllib
import apiclient
import re
import oauth2client
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import requests
import os
import xml.etree.ElementTree as ET
import csv
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

def search_keyword(keyword, video_per_keyword):
    '''
    Returns 
    '''
    videoIdlist = []
    youtube = build(os.getenv("YOUTUBE_API_SERVICE_NAME"), os.getenv("YOUTUBE_API_VERSION"), developerKey = os.getenv("DEVELOPER_KEY"))
    # Call the search.list method to retrieve results matching the specified query term.
    search_response = youtube.search().list(q = keyword, part = "id,snippet", maxResults = video_per_keyword).execute()
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
          videoIdlist.append(search_result["id"]["videoId"])
    
    return videoIdlist
 
def write_keyword_and_id(keyword_list, video_per_keyword):
    '''
    Returns a dataframe that includes the video id list 
    
    @params: keyword_list, the path of input keyword list
    '''
    
    result = pd.DataFrame(columns = ["keyword", "id", "rank"])
    for keyword in keyword_list: # segment your keywords and run the file sequentially (copy all individual files to Text-Data folder)
        print('Processing Keyword: ', keyword)
        try:
            videoIdlist = search_keyword(keyword_list, video_per_keyword)
            rank = 1
            for id in videoIdlist:
                result.loc[len(result.index)] = [keyword, id, rank] # insert keyword and id into result dataframe
                rank += 1

        except HttpError as e:
            print("The keyword is: ", keyword)
            print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))  

    # Drop duplicates based on id column, keep the last occurence since the dataframe is ranked based on keyword popularity
    result_no_duplicate = result.drop_duplicates(subset="id", keep="last")
    
    return result_no_duplicate
    
if __name__ == '__main__':
    keyword_list = ['Diabete', 'Causes']
    print(write_keyword_and_id(keyword_list, 2))
 