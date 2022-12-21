# Youtube Video Metadata Extraction Pipeline

## Project Introduction
Scripts for YouTube video downloading. 

### Metadata Extraction
Data pipeline to search youtube videos based on clinical keywords and extract video metadata.

#### Acc tag
This function extracts the accreditation tag of youtube videos. The accreditation tag is a new feature on YouTube that verifies authoritative sources for health related videos. You may find the details here:
https://support.google.com/youtube/answer/9795167

### Content Analysis
Transfer videos and metadata into features.

### Classification Model
Models to classifiy videos based on high/low understandability and high/low medical information.

## Authenticiate
There are multiple authentication that requires manual setup.

### PyTrends
Google trends.
Error handling:
1. https://stackoverflow.com/questions/50571317/pytrends-the-request-failed-google-returned-a-response-with-code-429

### search video id based on keywords
You need the Google Developer API to conduct this search. 
One account per day: search 91 keywords. Asked to increase quota.
#DEVELOPER_KEY = "AIzaSyANdt1eW-eYygBWMa73vtjX9G2XlvkIdAg" # original API KEY for project
#DEVELOPER_KEY = "AIzaSyBxztRZEw8u6EjuMgV77dBS1Soel5bOXnk" # Key for Ruoyu Zhang

### extract metadata based on video id
You need to put your credential for OAuth2.0 Client IDs. Download the credentials from the portal to credentials_and_keys folder and name it 'credential.json'. Remember to delete token.pickle file before you build a new connection. If you don't, it would cause an [invalid grant error] (https://stackoverflow.com/questions/10576386/invalid-grant-trying-to-get-oauth-token-from-google)

ytbvideoanalytics2022@gmail.com, 
PW: CMU15213!

If you 

### download videos to local
You need to include API key. 

### upload videos to cloud
You need include the credential for OAuth2.0 Client IDs. Besides, you need to create a bucket for uploading.
