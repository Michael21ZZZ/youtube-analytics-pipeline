'''
Scripts for downloading videos to local machine.
Notes:
    1. Update the Developer Key variable with your own key. You can find it here:
    https://cloud.google.com/docs/authentication/api-keys
'''
# coding: utf-8
from pytube import YouTube
import os
import json
import urllib
from googleapiclient import discovery
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import requests
import os
import xml.etree.ElementTree as ET
import csv
import pandas
import shutil

# Note: run the bash script named 'sleep.sh' to allow for continual download of videos

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
# https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.

# DEVELOPER_KEY = "AIzaSyBCo5JIrF4IPQ5jIjOBqUxBPS7IgBAEvfE" # original API KEY for project
#YOUTUBE_API_SERVICE_NAME = "youtube"
#YOUTUBE_API_VERSION = "v3"

# setting the base URL to concatenate video ID
BASE_URL = 'https://www.youtube.com/watch?v='
DEVELOPER_KEY = "AIzaSyBxztRZEw8u6EjuMgV77dBS1Soel5bOXnk" # Key for Ruoyu Zhang

# function that takes in a text file with video IDs and returns youtube URLs
def get_downloadURLSet(filename):
    URL_set = set()
    ID_set = []
    with open(filename) as f:
        for eachURL in f.readlines():
            eachURL = eachURL.rstrip('\n')
            URL_set.add(BASE_URL + eachURL)
            ID_set.append(eachURL)
            # print(eachURL)
    return URL_set, ID_set

# function that takes in a set of URLs and downloads in a folder called videos (action: create folder named videos in local dir)
def download_video(downloadURLSet, ID_set):
    # path = r"C:/Harris/CMU/Semester 4/Capstone Project/Data/Youtube-downloader-rema/videos/"
    print(len(downloadURLSet))
    if len(downloadURLSet) == 0:
        print("no video to download")
        return
    current_number = 0

    # create a folder called videos
    path = "./videos"
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)

    for downloadURL in downloadURLSet:
        print(downloadURL)
        try:
            yt = YouTube(downloadURL)
            name = yt.title
            oldName = name
            newName = ID_set[current_number]
            print("Now is loading %s------------>" % name)
            stream = yt.streams.filter(file_extension='mp4').first()
            stream.download('./videos/', filename = newName + '.mp4')
            # os.rename(path + oldName + '.mp4', path + oldName + '-' + newName + '.mp4')
            # os.rename(os.path.join('./videos', yt.streams.first().default_filename), os.path.join('./videos', downloadURL.strip(BASE_URL)+'.mp4'))
            print("--------------->%s is loaded!" % name)
            print(current_number)
            current_number += 1
        except:
            print("Some thing wrong about the authority!")
            continue
        print('Video downloaded .......')        

# main function
def main():
    URL_set, ID_set = get_downloadURLSet('videoIDs.txt')
    # print(URL_set)
    download_video(list(URL_set), ID_set)

if __name__ == '__main__':
    main()