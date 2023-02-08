from google.cloud import storage
import os
import argparse
import pprint

credential_path= "/credential_and_key/geometric-rock-358702-c152672f14dc.json"  # You have to create your own json credential
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getcwd() + credential_path
# UP_LOAD_FILE_ROUTE = './output/videos'
# BUCKET_NAME = 'youtube-video-bucket' # You have to create your bucket and download the bucket name
UP_LOAD_FILE_ROUTE = './output/audios'
BUCKET_NAME = 'youtube-audio-bucket' # You have to create your bucket and download the bucket name

# upload single file
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """
    Uploads a single file to the bucket.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

#upload multiple file
def upload_files(bucket_name):

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    file_names = os.listdir(UP_LOAD_FILE_ROUTE)
    for file1 in file_names:
        source_file_route = os.path.join(UP_LOAD_FILE_ROUTE, file1)
        blob = bucket.blob(file1)
        blob.upload_from_filename(source_file_route)
        print(
            "File {} uploaded to {}.".format(
                source_file_route, file1
            )
        )

# get bucket metadata
def bucket_metadata(bucket_name):
    """Prints out a bucket's metadata."""
    # bucket_name = 'your-bucket-name'

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    print("ID: {}".format(bucket.id))
    print("Name: {}".format(bucket.name))
    print("Storage Class: {}".format(bucket.storage_class))
    print("Location: {}".format(bucket.location))
    print("Location Type: {}".format(bucket.location_type))
    print("Cors: {}".format(bucket.cors))
    print(
        "Default Event Based Hold: {}".format(bucket.default_event_based_hold)
    )
    print("Default KMS Key Name: {}".format(bucket.default_kms_key_name))
    print("Metageneration: {}".format(bucket.metageneration))
    print(
        "Retention Effective Time: {}".format(
            bucket.retention_policy_effective_time
        )
    )
    print("Retention Period: {}".format(bucket.retention_period))
    print("Retention Policy Locked: {}".format(bucket.retention_policy_locked))
    print("Requester Pays: {}".format(bucket.requester_pays))
    print("Self Link: {}".format(bucket.self_link))
    print("Time Created: {}".format(bucket.time_created))
    print("Versioning Enabled: {}".format(bucket.versioning_enabled))
    print("Labels:")
    pprint.pprint(bucket.labels)

if __name__ == '__main__':
    #upload_blob(BUCKET_NAME, './output/videos/0.mp4', 'videos/0.mp4')
    upload_files(BUCKET_NAME)
