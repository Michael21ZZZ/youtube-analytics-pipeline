'''
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


def search_by_keywords(keyword, max_result):
    videoIdlist = []
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY)
    # Call the search.list method to retrieve results matching the specified query term.
    search_response = youtube.search().list(q = keyword, part = "id,snippet", maxResults = max_result).execute()
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
          videoIdlist.append(search_result["id"]["videoId"])
    
    return videoIdlist
    
def write_keyword_and_id(keyword_file, max_result):
    keyword_list = keyword_file.iloc[:, 0].tolist()
    result = pd.DataFrame(columns = ["keyword", "id", "rank"])
    for keyword in keyword_list: # segment your keywords and run the file sequentially (copy all individual files to Text-Data folder)
        print('Processing Keyword: ', keyword)
        try:
            videoIdlist = search_by_keywords(keyword, max_result)
            rank = 1
            for id in videoIdlist:
                result.loc[len(result.index)] = [keyword, id, rank] # insert keyword and id into result dataframe
                rank += 1

        except HttpError as e:
            print("The keyword is: ", keyword)
            print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))  

    # Drop duplicates based on id column, keep the last occurence since the dataframe is ranked based on keyword popularity
    result_no_duplicate = result.drop_duplicates(subset="id", keep="last")
    #result_no_duplicate.to_csv('./temp/videoIDs.csv',index=False)
    result_no_duplicate.to_csv('./temp/videoID_list.csv',index=False)

if __name__ == '__main__':
    DEVELOPER_KEY = 'AIzaSyCOjk3Drh1S6aYeOWKeYdUAtACFjKUTl8g'
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    max_result = 25

    keyword_file = pd.read_csv('./temp/top_100_keywords.csv')
    write_keyword_and_id(keyword_file, max_result)
 