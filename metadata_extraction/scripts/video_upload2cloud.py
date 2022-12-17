'''
Scripts for uploading videos to the GCP.
Notes:
    1. Use your own google credentials. Instructions on how to get credentials:
    https://cloud.google.com/docs/authentication/getting-started
    https://www.youtube.com/watch?v=th5_9woFJmk
    2. Build a new bucket on GCP and use the bucket name for uploading. Instructions on how to build buckets:
    https://cloud.google.com/appengine/docs/standard/python/googlecloudstorageclient/setting-up-cloud-storage
    https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-code-sample

'''

# Imports the Google Cloud client library
from google.cloud import storage
import os
import argparse
import pprint

# Run by command line prompt (include bucket_name)
# python Youtube_Upload2Cloud.py --bucket_name youtube-project-351220.appspot.com

# Original Scripts for video and audio downloading
# parser = argparse.ArgumentParser()
# parser.add_argument('--audio_path', type=str, default='./audios')
# parser.add_argument('--bucket_name', type=str, default='')
# args = parser.parse_args()
# UP_LOAD_FILE_ROUTE = './videos'
# BUCKET_NAME = args.bucket_name

# creating environment variable for google app credentials
# download the json to Scripts
######## Modify here
credential_path= "/youtube-project-351220-44b975bbe749.json"  # You have to create your own json credential
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getcwd() + credential_path

UP_LOAD_FILE_ROUTE = './videos'

######## Modify here
BUCKET_NAME = 'youtube-project-351220.appspot.com' # You have to create your bucket and download the bucket name

# upload single file
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )
# upload_blob('videos', './test.wav', 'test.wav')


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


# main function executing one task: upload files to metadata
def main():
    upload_files(BUCKET_NAME)

if __name__ == '__main__':
	main()

