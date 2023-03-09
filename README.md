# Youtube Video Analytics Platform

## Introduction

This platform is used for YouTube videos. It consists of three parts:

1. Video selection. Search youtube videos based on clinical keywords
2. Feature extraction. YouTube provides a powerful API, YouTube Data API, to help developers and researchers collect key features on YouTube videos which we categorize as intrinsic and extrinsic features. Intrinsic features can be considered as properties of the video such as its duration, language, and so on that remain static over time. Extrinsic features are exogenous to the video such as the number of views, likes and comments that change over time once the video is published. ![image](https://user-images.githubusercontent.com/91205016/224120047-069ef879-a098-4c6d-bc95-5795bb30f575.png)

3. Classification. Train a model to classifiy videos based on high/low understandability and high/low medical information.

The overall data pipeline is shown as follows:

![Data Pipeline](https://user-images.githubusercontent.com/91205016/218861007-9bbc343a-af1a-4411-95b3-4bd0308fe9f7.jpg)

## Installation
Download the whole scripts by...

## Authenticiate
There are multiple authentication that requires manual setup.

### Account use
The Google account for this project is ytbvideoanalytics2022@gmail.com. The password is CMU15213!. 

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
You need to put your credential for OAuth2.0 Client IDs. Download the credentials from the portal to credentials_and_keys folder and name it 'credential.json'. Remember to delete token.pickle file before you build a new connection. If you don't, it would cause an [invalid grant error](https://stackoverflow.com/questions/10576386/invalid-grant-trying-to-get-oauth-token-from-google)

### download videos to local
You need to include API key. 

### upload videos to cloud
You need include the credential for OAuth2.0 Client IDs. Besides, you need to create a bucket for uploading.

## Notes
### Acc tag
This function extracts the accreditation tag of youtube videos. The accreditation tag is a new feature on YouTube that verifies authoritative sources for health related videos. You may find the details here:
https://support.google.com/youtube/answer/9795167

