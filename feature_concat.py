import json

if __name__ == "__main__":
    index  = 0
    dict_output = {}
    # load from metadata feature
    dict_metadata = json.load("./output/final_data.json".read())
    # load from transcription feature, which only includes transcription confidence
    dict_transcription = json.load("./output/transcription_feature.json".read())
    # load from video feature, 3 features
    dict_video = json.load("./output/video_feature.json".read())
    # load from text feature, 14 features

    # extract output features
    dict_output['views'] = dict_metadata[index]['views']
    dict_output['channel_subscribers'] = dict_metadata[index]['durations']
    
    # 