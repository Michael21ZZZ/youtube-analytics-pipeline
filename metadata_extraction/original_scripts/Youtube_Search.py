'''
Scripts to search videos according to keywords.
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
import pandas
import isodate

# importing the metadata code
from Youtube_Metadata import *

# DEVELOPER_KEY = "AIzaSyANdt1eW-eYygBWMa73vtjX9G2XlvkIdAg" # original API KEY for project
DEVELOPER_KEY = "AIzaSyBxztRZEw8u6EjuMgV77dBS1Soel5bOXnk" # Key for Ruoyu Zhang
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


# takes in a keyword and yields 40 video IDs by default
def youtube_search(query, max_result = 40):
    videoIdlist = []
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY)
    # Call the search.list method to retrieve results matching the specified query term.
    search_response = youtube.search().list(q = query, part = "id,snippet", maxResults = max_result).execute()
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
          videoIdlist.append(search_result["id"]["videoId"])
    shortVideoList = {}
    desc_dict = {}
    for videoID in videoIdlist:
        video = {}
        search_response={}
        try:
            search_response=youtube.videos().list(part="id, snippet,contentDetails", id=videoID).execute()
            if search_response['pageInfo']['totalResults']!=1:
                print("no result/not unique ID.")
            else:
                for item in search_response.get("items", []):
                    video['contentDuration']=item['contentDetails']['duration']
                    desc_dict[str(videoID)]=item['snippet']['description']
        # filtering the large videoIDlist to create a sub-list based on duration filter 
            time = video["contentDuration"]
            time_seconds = isodate.parse_duration(time).total_seconds()
            if (time_seconds < 361 and time_seconds > 59):
                shortVideoList[str(videoID)] = time_seconds 
        except Exception as e:
            print('Problem occurred')
            print('An exception occurred: ', e)
    return shortVideoList, desc_dict


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
    cosine = c / float((sum(l1)*sum(l2))**0.5)
    # print("similarity: ", cosine)
    return(cosine)


# function which takes keywords file as input and write the video IDs for the videos as output
# and writes dictionary of metadata for the corresponding videos into a text file 
def get_videos(keyword, max_result):
    try:
        output, desc_dict=youtube_search(keyword,max_result)
        videoIdlist = []
        for idx, value in output.items():
            videoIdlist.append(idx)
        with open('videoIDs' + '.txt', 'a') as f:
            for i in videoIdlist:
                f.write(i)
                f.write('\n')
        f = open('complete_data.txt','a')
        rank = 0
        for idx, value in output.items():
            result = youtube_get_videoinfo(idx)
            result['duration'] = value
            result['keyword']=str(keyword, 'utf-8')
            rank += 1
            result['rank']=rank
            d_unicode = desc_dict[idx].replace('\n', '')
            d_encode = d_unicode.encode("ascii", "ignore")
            d_decode = d_encode.decode()
            result['description'] = d_decode

            try:
                if(len(result['description']) > 0):
                    result['cosine_similarity'] = calc_cosine_similarity(str(keyword), result['description'])
                else:
                    result['cosine_similarity'] = 0
            except:
                result['cosine_similarity'] = 0
                print('Description exception!')
            f.write(json.dumps(result))
            f.write('\n')
        f.close() 
    except HttpError as e:
        print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))    


# main function executing two tasks: writing a text file with metadata & writing a text file with video IDs only
def main():
    keywords_file = pandas.read_csv('NewList_OSA_Patient.csv')
    L1 = keywords_file.iloc[:, 0].tolist()
    for keyword in L1: # segment your keywords and run the file sequentially (copy all individual files to Text-Data folder)
        print('Processing Keyword: ', keyword)
        get_videos(keyword.encode("utf-8"), max_result = 5) #extracting 40 videos per keyword


if __name__ == '__main__':
    main()
    print('Finish Video Searching.')
