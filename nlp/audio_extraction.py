import os
from moviepy.editor import VideoFileClip

def extract_audio_from_video(video_path, audio_path):
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

if __name__ == '__main__':
    VIDEO_PATH = "./output/videos"
    AUDIO_PATH = "./output/audios"
    video_list = os.listdir(VIDEO_PATH)
    extract_audio_from_video(VIDEO_PATH, AUDIO_PATH)