import pandas as pd
import os
import json
import pprint
from google.cloud import storage
from dotenv import load_dotenv 
import redis
import multiprocessing
from feature.video import *
from feature.audio import *
from feature.metadata import *
from feature.setup import *
from feature.nlp import *
import time

# Connect to the Redis server
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Define a function to check whether setup process has completed successfully for a specific video
def check_setup_status(video_id):
    # Check if the video setup status is already cached in Redis
    if redis_client.hexists(video_id, 'setup_status'):
        return redis_client.hget(video_id, 'setup_status') == b'success'
    else:
        # Perform the setup process and cache the setup status in Redis
        try:
            download(video_id)
            redis_client.hset(video_id, 'setup_status', 'success')
            return True
        except DownloadError as e:
            redis_client.hset(video_id, 'setup_status', 'error')
            return False
        
# Define a function to extract features for a single video and store it to redis
def extract_features(video_id):
    print()
    print('Start extraction: ', video_id)
    # Record the start time
    start_time = time.time()
    try: 
        youtube = youtube_authenticate(os.environ.get("OAUTH_CREDENTIAL_PATH"))
        
    except AuthenticateError:
        print('Authenticate Error!')
        return
    
    # Check whether the setup process has completed successfully for this video
    if not check_setup_status(video_id):
        print(f'Error: setup process failed for video {video_id}')
        return
    
    # collect metadata
    if redis_client.hget(video_id, 'metadata_status') == b'success':
        description = redis_client.hget(video_id, 'description').decode('utf8')
    else:
        try: 
            metadata = metadata_features(youtube = youtube, video_id = video_id)
            description = metadata['description']
            redis_client.hset(video_id, 'metadata_status', 'success')
            for k, v in metadata.items():
                redis_client.hset(video_id, k, v)
        except MetadataError as e:
            redis_client.hset(video_id, 'metadata_status', 'fail')
            print(e.message)
        
    # collect video features
    if redis_client.hget(video_id, 'video_status') == b'success':
       pass
    else:
        try: 
            gcs_video_path = os.path.join("gs://", os.environ.get("VIDEO_BUCKET_NAME"), video_id +".mp4")
            video = analyze_by_path(gcs_video_path)
            redis_client.hset(video_id, 'video_status', 'success')
            for k, v in video.items():
                redis_client.hset(video_id, k, v)
        except:
            redis_client.hset(video_id, 'video_status', 'fail')
            print('video fails')
    
    # collect audio features
    if redis_client.hget(video_id, 'audio_status') == b'success':
        transcription = redis_client.hget(video_id, 'transcription').decode('utf8')
    else:
        try:
            gcs_audio_path = os.path.join("gs://", os.environ.get("AUDIO_BUCKET_NAME"), video_id +".wav")
            audio = transcribe_gcs(gcs_audio_path)
            transcription = audio['transcription']
            redis_client.hset(video_id, 'audio_status', 'success')
            for k, v in audio.items():
                redis_client.hset(video_id, k, v)
        except:
            redis_client.hset(video_id, 'audio_status', 'fail')  
            print('audio fails')
        
    # collect nlp features
    if redis_client.hget(video_id, 'nlp_status') == b'success':
        pass
    else:
        try: 
            nlp = dict()
            desc_nlp = desc_nlp_feature(description)
            trans_nlp = trans_nlp_feature(transcription)
            nlp.update(desc_nlp)
            nlp.update(trans_nlp)
            redis_client.hset(video_id, 'nlp_status', 'success')
            for k, v in nlp.items():
                redis_client.hset(video_id, k, v)
        except:
            redis_client.hset(video_id, 'nlp_status', 'fail')
            print('nlp fails')  
    
    # Record the end time and calculate the elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time  
    redis_client.hset(video_id, 'last_time_used', elapsed_time)
    
    print('End extraction: ', video_id) 
    print()

# how to get video info from redis
def get_video_info(video_id):
    # Retrieve the video information from Redis
    video_info = redis_client.hgetall(video_id)

    # Convert the values from bytes to strings and deserialize the JSON values
    result = dict()
    for key, value in video_info.items():
        result[key.decode('utf-8')] = value.decode('utf-8')
    
    return result

# Define a callback function to print a message when a worker process starts
def start_callback(process_index):
    print(f'Worker process {process_index} started')

# Define a callback function to print a message when a worker process stops
def stop_callback(process_index):
    print(f'Worker process {process_index} stopped')
    
# Define a function to download features for multiple videos in parallel
def extract_features_parallel(video_ids):
    num_processes = 4
    # Use multiprocessing to extract features in parallel
    with multiprocessing.Pool(processes=num_processes, initializer=start_callback, initargs=([i for i in range(num_processes)],)) as pool:
        pool.map(extract_features, video_ids, chunksize=10)
        pool.close()
        pool.join()
        stop_callback([i for i in range(num_processes)])

if __name__ == '__main__':
    # Load environment variables from the .env file
    load_dotenv("ytbvideoanalytics2022.env", override=True)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.getcwd(), os.environ.get("SERVICE_ACCOUNT_PATH"))
    # load the covid dataset
    colon = pd.read_csv("input/Yawen-Colonoscopy-Covid Data files/colonoscopy/complete_colonoscopy_classification_set.csv")
    colon_list = colon['id'].values.tolist()
    extracted_keys = [item.decode('utf-8') for item in redis_client.scan(match='*', count=1000)[1]]
    unextracted_keys = [item for item in colon_list if item not in extracted_keys]
    extract_features_parallel(unextracted_keys)

