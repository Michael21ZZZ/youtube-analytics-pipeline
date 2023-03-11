import pandas
import os
import sys
from dotenv import load_dotenv
import json
import pandas as pd
import pprint
from video_selection.google_trends import get_trends
from video_selection.search_by_keyword import write_keyword_and_id
from video_selection.filter import filter_sample_videos
from feature.metadata import metadata_extraction
from feature.metadata import youtube_authenticate
from feature.video import analyze_by_path
from feature.audio import transcribe_gcs
from feature.nlp import *
from datetime import datetime

class FeatureError(Exception):
    def __init__(self, message):
        self.message = message
    
def feature_extraction(video_id):   
    try:
        print("\nSTARTING FEATURE EXTRACTION ON: ", video_id)
        # authenticate
        youtube = youtube_authenticate(os.environ.get("OAUTH_CREDENTIAL_PATH"))
        # gcs path
        gcs_video_path = os.path.join("gs://", os.environ.get("VIDEO_BUCKET_NAME"), video_id +".mp4")
        gcs_audio_path = os.path.join("gs://", os.environ.get("AUDIO_BUCKET_NAME"), video_id +".wav")
    except:
        raise FeatureError('HAVING TROBULE WITH AUTHENTICATION: ' + video_id)
    
    # try: 
    #     print("EXTRACTING RAW METADATA FEATURES!")
    #     metadata = metadata_extraction(youtube, video_id) # in json file
    #     with open("temp/covid-metadata/" + video_id + ".json", "w") as outfile:
    #         json.dump(metadata, outfile)
    # except:
    #     raise FeatureError('HAVING TROBULE WITH RAW METADATA EXTRACTION: ' + video_id)
    
    try: 
        # gcs path
        gcs_video_path = os.path.join("gs://", os.environ.get("VIDEO_BUCKET_NAME"), video_id +".mp4")
        gcs_audio_path = os.path.join("gs://", os.environ.get("AUDIO_BUCKET_NAME"), video_id +".wav")
        print("EXTRACTING VIDEO AND AUDIO FEATURES!")
        # video feature, 4 minutes for a video
        video = analyze_by_path(gcs_video_path)
        # transcription feature, 1 min 30 s for a video
        audio = transcribe_gcs(gcs_audio_path)
        video.update(audio)
        with open("temp/covid-av/" + video_id + ".json", "w") as outfile:
            json.dump(video, outfile)
    except:
        raise FeatureError('HAVING TROBULE WITH VIDEO AND AUDIO FEATURES: ' + video_id)
    
    try: 
        print("EXTRACTING NLP FEATURES!")
        # nlp feature
        nlp = {}
        # syntatic features of desccription and transcription
        nlp['desc_words'],nlp['desc_uni'],nlp['desc_sen'],nlp['desc_act'], nlp['desc_sum'], nlp['desc_trans'], nlp['desc_ari'] = count_stats(metadata['description'])
        nlp['tran_words'],nlp['tran_uni'],nlp['tran_sen'],nlp['tran_act'], nlp['tran_sum'], nlp['tran_trans'], nlp['tran_ari'] = count_stats(audio['transcription'])
        # mer features of description and transcription
        nlp['desc_mer'] = medical_entity_count(metadata['description'])
        nlp['tran_mer'] = medical_entity_count(audio['transcription'])
        # cosine similarity feature
        # nlp['cos_desc'] = calculate_cosine_similarity(keyword, metadata['description'])
        # nlp['cos_trans'] = calculate_cosine_similarity(keyword, audio['transcription'])
        # nlp['cos_title'] = calculate_cosine_similarity(keyword, metadata['title'] + metadata['tags'])
        with open("temp/covid-nlp/" + video_id + ".json", "w") as outfile:
            json.dump(nlp, outfile)
    except:
        raise FeatureError('HAVING TROBULE WITH NLP FEATURES: ' + video_id)
    
    print("CONCATENATE ALL FEATURES!")

    # concat all features
    merged_feature = {}
    merged_feature.update(metadata)
    merged_feature.update(video)
    merged_feature.update(audio)
    merged_feature.update(nlp)

    # drop unnecessary columns
    merged_feature.pop('description')
    merged_feature.pop('transcription')
    merged_feature.pop('title')
    
    return merged_feature

    # pprint.pprint(merged_feature)

