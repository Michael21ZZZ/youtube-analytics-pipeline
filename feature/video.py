from google.cloud import videointelligence
import os
import json

# the number of shot changes is extracted via ShotChangeDetection
def analyze_shots(path):
    """Detects camera shot changes."""
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.SHOT_CHANGE_DETECTION]
    operation = video_client.annotate_video(
        request={"features": features, "input_uri": path}
    )
    print("Processing video for shot change annotations:")

    result = operation.result(timeout=120)
    print("Finished processing.")
    
    num_shots = sum(1 for _ in result.annotation_results[0].shot_annotations)
     
    return num_shots


# number of unique objects is extracted from ObjectTracking
def analyze_objects(path):
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.OBJECT_TRACKING]
    operation = video_client.annotate_video(
        request={"features": features, "input_uri": path}
    )
    print("Processing video for object annotations.")

    result = operation.result(timeout=500)
    print("Finished processing.\n")
    
    # The first result is retrieved because a single video was processed.
    object_annotations = result.annotation_results[0].object_annotations
    num_of_objects = sum(1 for _ in object_annotations)
    
    return num_of_objects
    
# text detection confidence is extracted from TextDetection
def text_detection(path):
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.TEXT_DETECTION]
    
    operation = video_client.annotate_video(request={"features": features, "input_uri": path})

    print("Processing video for text detection.")
    result = operation.result(timeout=600)

    # The first result is retrieved because a single video was processed.
    annotation_result = result.annotation_results[0]
    confidence = 0
    num_of_texts = sum(1 for _ in annotation_result.text_annotations)

    for text_annotation in annotation_result.text_annotations:
        # Get the first text segment
        text_segment = text_annotation.segments[0]
        confidence += text_segment.confidence
    
    if num_of_texts == 0:
        return 0
    else:
        return confidence / num_of_texts
        
def analyze_by_path(path):
    dict_video = {}
    # dict_video['id'] = os.path.basename(path).split(".")[0]
    dict_video['num_of_shots'] = analyze_shots(path)
    dict_video['num_of_objects'] = analyze_objects(path)
    dict_video['text_confidence'] = text_detection(path)
    
    return dict_video
    
if __name__ == "__main__":
    path = "gs://youtube-video-bucket/0.mp4"
    print(analyze_by_path(path))
    # with open('./temp/video_feature.json', "w") as f:
    #     json.dump(dict_video, f)
    #     f.write('\n')
    # f.close()
