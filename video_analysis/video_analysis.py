from google.cloud import videointelligence
import os
import json
credential_path= "/credential_and_key/geometric-rock-358702-c152672f14dc.json"  # You have to create your own json credential
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getcwd() + credential_path

# the number of shot changes is extracted via ShotChangeDetection
def analyze_shots(path):
    """Detects camera shot changes."""
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.SHOT_CHANGE_DETECTION]
    operation = video_client.annotate_video(
        request={"features": features, "input_uri": path}
    )
    print("\nProcessing video for shot change annotations:")

    result = operation.result(timeout=120)
    print("\nFinished processing.")
    
    num_shots = sum(1 for _ in result.annotation_results[0].shot_annotations)
    
    # for i, shot in enumerate(result.annotation_results[0].shot_annotations):
    #     start_time = (
    #         shot.start_time_offset.seconds + shot.start_time_offset.microseconds / 1e6
    #     )
    #     end_time = (
    #         shot.end_time_offset.seconds + shot.end_time_offset.microseconds / 1e6
    #     )
    #     print("\tShot {}: {} to {}".format(i, start_time, end_time))
    
    return num_shots




# number of unique objects is extracted from ObjectTracking
def analyze_objects(path):
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.OBJECT_TRACKING]
    operation = video_client.annotate_video(
        request={"features": features, "input_uri": path}
    )
    print("\nProcessing video for object annotations.")

    result = operation.result(timeout=500)
    print("\nFinished processing.\n")
    
    # The first result is retrieved because a single video was processed.
    object_annotations = result.annotation_results[0].object_annotations
    num_of_objects = sum(1 for _ in object_annotations)
    
    return num_of_objects
    
    

# text detection confidence is extracted from TextDetection
def text_detection(path):
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.TEXT_DETECTION]
    
    operation = video_client.annotate_video(request={"features": features, "input_uri": path})

    print("\nProcessing video for text detection.")
    result = operation.result(timeout=600)

    # The first result is retrieved because a single video was processed.
    annotation_result = result.annotation_results[0]
    confidence = 0
    num_of_texts = sum(1 for _ in annotation_result.text_annotations)

    for text_annotation in annotation_result.text_annotations:
        # Get the first text segment
        text_segment = text_annotation.segments[0]
        confidence += text_segment.confidence
    
    return confidence / num_of_texts
        

if __name__ == "__main__":
    path = "gs://youtube-video-bucket/0.mp4"
    dict_video = {}
    dict_video['num_of_shots'] = analyze_shots(path)
    dict_video['num_of_objects'] = analyze_objects(path)
    dict_video['text_confidence'] = text_detection(path)
    with open('./temp/video_feature.json', "w") as f:
        json.dump(dict_video, f)
        f.write('\n')
    f.close()
