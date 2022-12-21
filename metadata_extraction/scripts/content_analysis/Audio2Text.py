import sys
import os, io
from moviepy.editor import *
video_id_list = os.listdir(VIDEO_PATH)

audio_id_list = os.listdir(AUDIO_PATH)
audio_id_list = [a.split(".")[0] for a in audio_id_list]

for video_id in video_id_list:
    if 'mp4' in video_id and video_id.split(".")[1] == "mp4":
        if video_id.split(".")[0] not in audio_id_list:
          try:
              video = VideoFileClip(os.path.join(VIDEO_PATH, video_id))
              audio = video.audio
              audio_id = video_id.replace('.mp4', '.wav')
              audio.write_audiofile(os.path.join(AUDIO_PATH, audio_id))
              video.close()
              audio.close()
          except:
              print('can not extract from ', video_id)
    VIDEO_PATH = "videos/videos_final"
    AUDIO_PATH = "text/audios-wav"
    return
             
def extract_audio_from_video(video_path):
    '''
    Exfract the audio from a single video.
    '''
    # assign video path and audio path here


def extract_text_from_video
    '''
    '''
    return


              
if __name__ == 'main':
    