from google.cloud import storage,speech
import os
import json
credential_path= "/credential_and_key/geometric-rock-358702-c152672f14dc.json"  # You have to create your own json credential
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getcwd() + credential_path
BUCKET_NAME = 'youtube-audio-bucket' # You have to create your bucket and download the bucket name


# [START speech_transcribe_sync_gcs]
def transcribe_gcs(gcs_uri):
    """Transcribes the audio file specified by the gcs_uri."""
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

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)
    
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    transcription = ''
    confidence = 0
    num_result = 0
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print("Transcript: {}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))
        transcription += result.alternatives[0].transcript
        confidence += result.alternatives[0].confidence
        num_result += 1
    avg_confidence = confidence / num_result
    return transcription, avg_confidence
        
    
# [END speech_transcribe_sync_gcs]

if __name__ == "__main__":
    path = "gs://youtube-audio-bucket/0.wav"
    transcription, avg_confidence = transcribe_gcs(path)
    dict_trans = {}
    dict_trans['text'] = transcription
    dict_trans['confidence'] = avg_confidence
    with open('./output/transcription_feature.json', "w") as f:
        json.dump(dict_trans, f)
        f.write('\n')
    f.close()

