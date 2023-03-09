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

# transcribe on gcp
def transcribe_gcs(gcs_uri):
    """
    Transcribes the audio file specified by the gcs_uri.
    
    @param gcs_uri
    """
    client = speech.SpeechClient()

    # [START speech_python_migration_config_gcs]
    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        #encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        language_code="en-US",
        audio_channel_count = 2
    )
    # [END speech_python_migration_config_gcs]
    operation = client.long_running_recognize(config=config, audio=audio)

    # print("Waiting for operation to complete...")
    # 180 is not enough...
    response = operation.result(timeout=600) # timeout
    
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    transcription = ''
    confidence = 0
    num_result = 0
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        # print("Transcript: {}".format(result.alternatives[0].transcript))
        # print("Confidence: {}".format(result.alternatives[0].confidence))
        transcription += result.alternatives[0].transcript
        confidence += result.alternatives[0].confidence
        num_result += 1
    avg_confidence = confidence / num_result
    
    dict_trans = {}
    dict_trans['id'] = os.path.basename(gcs_uri).split(".")[0]
    dict_trans['transcription'] = transcription
    dict_trans['transcription confidence'] = avg_confidence
    
    return dict_trans
        
if __name__ == "__main__":
    path = "gs://youtube-audio-bucket/0.wav"
    dict = transcribe_gcs(path)
    # with open('./output/transcription_feature.json', "w") as f:
    #     json.dump(dict_trans, f)
    #     f.write('\n')
    # f.close()

