import json

if __name__ == "__main__":
    index  = 0
    dict_output = {}
    dict_metadata = json.load("./output/final_data.json".read())
    dict_transcription = json.load("./output/transcription_feature.json".read())
    dict_video = json.load("./output/video_feature.json".read())
    # extract output features
    dict_output['views'] = dict_metadata[index]['views']
    dict_output['channel_subscribers'] = dict_metadata[index]['durations']
    
    