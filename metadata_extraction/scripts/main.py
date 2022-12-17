import sys
import pandas as pd

from google_trends import get_trends
import search
import metadata
from merge_input_list import merge_input_list

#Input Setting
keyword_ref = 'diabetes causes' # use the first keyword for comparison in each iteration. Suggestion: "Disease name + causes"
max_result_num = 25
patient_keyword_path = './input/input_list_patient.csv'
physician_keyword_path = './input/input_list_physician.csv'
combined_path = './input/input_list.csv'

#Credentials and keys
DEVELOPER_KEY = 'AIzaSyBxztRZEw8u6EjuMgV77dBS1Soel5bOXnk' # Key for Ruoyu Zhang
credential_path = '/youtube-project-351220-44b975bbe749.json' # You have to create your own json credential
BUCKET_NAME = 'youtube-project-351220.appspot.com' # You have to create your bucket and download the bucket name

if __name__ == 'main':
    merge_input_list(filepath1=patient_keyword_path, filepath2=physician_keyword_path)
    get_trends(keyword_path=combined_path, keyword_ref=keyword_ref, num_result=100)
    df_top_100_keywords = pd.read_csv('./temp/top_100_keywords.csv')
    


# google trends
# google_trends.get_trends(keyword_path, keyword_ref)

# # Running google search and return videoID.txt
# keyword_file = pd.read_csv('./temp/NewList.csv')
# search.write_keyword_and_id(keyword_file, max_result_num)

# # extract metadata based on videoID.txt

# # Download the video to local machine
# Youtube_Downloader.main()

# # Upload the video to GCP platform 
# Youtube_Upload2Cloud.main()


