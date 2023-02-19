'''
Download the video, Extract audio, and Upload the video and audio to GCP
'''
from google.cloud import storage,speech
import os
import json
import os
from moviepy.editor import VideoFileClip
from google.cloud import storage
import os
import argparse
import pprint
from pytube import YouTube
import pandas as pd
from google.cloud import storage
import os
import argparse
import pprint

credential_path= "/credential_and_key/geometric-rock-358702-c152672f14dc.json"  # You have to create your own json credential
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getcwd() + credential_path
BUCKET_NAME = 'youtube-audio-bucket' # You have to create your bucket and download the bucket name
LOCAL_VIDEO_PATH = "temp/videos"
LOCAL_AUDIO_PATH = "temp/audios"

def download_video_by_id(video_id, save_path):
    video_url = 'https://www.youtube.com/watch?v=' + video_id
    file_name = str(video_id) + '.mp4'
    print("Downloading:", video_url)
    try: 
        # object creation using YouTube which was imported in the beginning 
        yt = YouTube(video_url) 
    except: 
        print("Connection Error") #to handle exception 
    try: 
        # downloading the video 
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download(save_path, filename = file_name)
    except: 
        print("Some Error with the url!", video_url) 
    print('Video successfully downloaded!') 
    
    return os.path.join(save_path, file_name)

def extract_single_audio(video_path, audio_path):
    '''
    Extract audio from a local video and store it to the path.
    
    @param video_path: the local path of the video
    @param audio_path: the local path of the extracted audio
    '''
    
    video_name = os.path.basename(video_path)
    audio_name = video_name.replace('.mp4', '.wav')
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(os.path.join(audio_path, audio_name))
        video.close()
        audio.close()
    except:
        print('can not extract from ', video_name)
    
def extract_audios_from_videos(video_path, audio_path):
    '''
    Extract audios from all video in video_path and store it in audio-path
    '''
    video_list = os.listdir(video_path)
    if not os.path.exists(audio_path):
        os.makedirs(audio_path)
    for video_name in video_list:
        try:
            video = VideoFileClip(os.path.join(video_path, video_name))
            audio = video.audio
            audio_name = video_name.replace('.mp4', '.wav')
            audio.write_audiofile(os.path.join(audio_path, audio_name))
            video.close()
            audio.close()
        except:
            print('can not extract from ', video_name)

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """
    Uploads a single file to the bucket.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )
    
#upload multiple file
def upload_files(bucket_name, source_file_route):

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    file_names = os.listdir(source_file_route)
    for file1 in file_names:
        source_file_route = os.path.join(source_file_route, file1)
        blob = bucket.blob(file1)
        blob.upload_from_filename(source_file_route)
        print(
            "File {} uploaded to {}.".format(
                source_file_route, file1
            )
        )

# get bucket metadata
def bucket_metadata(bucket_name):
    """Prints out a bucket's metadata."""
    # bucket_name = 'your-bucket-name'

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    print("ID: {}".format(bucket.id))
    print("Name: {}".format(bucket.name))
    print("Storage Class: {}".format(bucket.storage_class))
    print("Location: {}".format(bucket.location))
    print("Location Type: {}".format(bucket.location_type))
    print("Cors: {}".format(bucket.cors))
    print(
        "Default Event Based Hold: {}".format(bucket.default_event_based_hold)
    )
    print("Default KMS Key Name: {}".format(bucket.default_kms_key_name))
    print("Metageneration: {}".format(bucket.metageneration))
    print(
        "Retention Effective Time: {}".format(
            bucket.retention_policy_effective_time
        )
    )
    print("Retention Period: {}".format(bucket.retention_period))
    print("Retention Policy Locked: {}".format(bucket.retention_policy_locked))
    print("Requester Pays: {}".format(bucket.requester_pays))
    print("Self Link: {}".format(bucket.self_link))
    print("Time Created: {}".format(bucket.time_created))
    print("Versioning Enabled: {}".format(bucket.versioning_enabled))
    print("Labels:")
    pprint.pprint(bucket.labels)

if __name__ == 'main':
    extract_single_audio("temp/KLoaYPXlWHM.mp4", "temp")