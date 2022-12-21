'''
Scripts for downloading YouTube videos to local machine based on a list of video ids.
'''

from pytube import YouTube
import pandas as pd

# where to save 
SAVE_PATH = "./output/videos/" 

def add_url(id):
    url_link = 'https://www.youtube.com/watch?v='
    return url_link + id

def download_video_by_id(video_id, current_number):
    video_url = add_url(video_id)
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
        print("Some Error with the url!", video_url) 
    print('Video successfully downloaded!') 
  

if __name__ == '__main__':
    final_data = pd.read_json('./output/final_data.json', lines = True)
    for i in range(final_data.shape[0]):
        video_id = final_data['id'].iloc[i]
        download_video_by_id(video_id, i)
