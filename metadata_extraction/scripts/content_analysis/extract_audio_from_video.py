import sys
import os, io
from moviepy.editor import VideoFileClip

def extract_audio_from_video(video_num_list, aduio_num_list):
    for video_num in video_num_list:
        if 'mp4' in video_num and video_num.split(".")[1] == "mp4":
            if video_num.split(".")[0] not in audio_num_list:
                try:
                    video = VideoFileClip(os.path.join(VIDEO_PATH, video_num))
                    audio = video.audio
                    audio_num = video_num.replace('.mp4', '.wav')
                    audio.write_audiofile(os.path.join(AUDIO_PATH, audio_num))
                    video.close()
                    audio.close()
                except:
                    print('can not extract from ', video_num)

if __name__ == 'main':
    VIDEO_PATH = "./output/videos"
    AUDIO_PATH = "./output/audios"
    video_num_list = os.listdir(VIDEO_PATH)
    audio_num_list = os.listdir(AUDIO_PATH)
    audio_num_list = [a.split(".")[0] for a in audio_num_list]
    extract_audio_from_video(video_num_list, audio_num_list)