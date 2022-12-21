'''
Scripts for downloading videos to local machine.
Notes:
    1. Update the Developer Key variable with your own key. You can find it here:
    https://cloud.google.com/docs/authentication/api-keys
'''

from fileinput import filename
from pytube import YouTube
import pandas as pd
from googleapiclient import discovery
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import xml.etree.ElementTree as ET

# where to save 
SAVE_PATH = "./videos_new/" 

def download_video_by_url(video_url, current_number):
    print("Downloading:", video_url)
    try: 
        # object creation using YouTube which was imported in the beginning 
        yt = YouTube(video_url) 
    except: 
        print("Connection Error") #to handle exception 
    try: 
        # downloading the video 
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download(SAVE_PATH, filename = str(current_number) + '.mp4')
    except: 
        print("Some Error!") 
    print('Task Completed!') 
  

if __name__ == '__main__':
    url_df = pd.read_excel("./url_list_new.xlsx")
    url = url_df['url'].iloc[0]
    for i in range(url_df.shape[0]):
        try:
            url = url_df['url'].iloc[i]
            print(i)
            print(url)
            download_video_by_url(url, i)
        except:
            print("Something wrong with link", url)
