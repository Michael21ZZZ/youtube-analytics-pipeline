'''
Scripts to prepare for metadata extraction.
Notes:
    1. Download chromedriver and add the chromedriver to the path. You may refer to
    https://www.browserstack.com/guide/run-selenium-tests-using-selenium-chromedriver#:~:text=Go%20to%20the%20terminal%20and,Type%20Y%20to%20save
    2. Do not use Spyder or Jupyternotebook to run this script since it will create errors. Pycharm is fine.
'''
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import sys
import os
import json
import pickle
import time
import re
from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession, AsyncHTMLSession

#for cosine similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import asyncio
import nest_asyncio

def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []
    # KEY_VALUE = ''
    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                # print(item)
                if(key in item):
                    # print(key, item[key])
                    # print('found key')
                    # KEY_VALUE = item[key]
                    arr.append(item[key])
                else:
                    extract(item, arr, key)
        return(arr)

    values = extract(obj, arr, key)
    return values

# takes in a video ID and yields the a dictionary called result - containing all metadata
def youtube_get_videoinfo(videoID):
    #initialize the result
    result = {}
    try:
        search_url = "https://www.youtube.com/watch?v="
        video_url = search_url + videoID
        # print('\n')
        print("Reading URL: ", video_url)

        # init an HTML Session
        session = HTMLSession()

        # get the html content
        response = session.get(video_url)
        # #change timeout
        # response.html.render(timeout=20)
        # execute Java-script
        response.html.render(scrolldown = 4, sleep=1, timeout=60)
        # create bs object to parse HTML
        soup = bs(response.html.html, "html.parser")
        print('soup')
        # time out error
        # response.html.render(sleep=1, timeout=60)
        # video ID
        result["id"] = soup.find("meta", itemprop="videoId")['content']
        # video title
        result["title"] = soup.find("meta", itemprop="name")['content']
        # video views (converted to integer)
        result["views"] = soup.find("meta", itemprop="interactionCount")['content']
        # date published
        result["date_published"] = soup.find("meta", itemprop="datePublished")['content']
        # get the video tags
        result["tags"] = ', '.join([meta.attrs.get("content") for meta in soup.find_all("meta", {"property": "og:video:tag"}) ])
        # Additional video and channel information 
        data = re.search(r"var ytInitialData = ({.*?});", soup.prettify()).group(1)
        data_json = json.loads(data)

        videoPrimaryInfoRenderer = json_extract(data_json, 'videoPrimaryInfoRenderer')
        videoSecondaryInfoRenderer = json_extract(data_json, 'videoSecondaryInfoRenderer')
        likes_label = videoPrimaryInfoRenderer[0]['videoActions']['menuRenderer']['topLevelButtons'][0]['toggleButtonRenderer']['defaultText']['accessibility']['accessibilityData']['label'] # "No likes" or "###,### likes"
        likes_str = likes_label.split(' ')[0].replace(',','')
        result["likes"] = '0' if likes_str == 'No' else likes_str

        # channel details
        channel_tag = soup.find("meta", itemprop="channelId")['content']
        # channel name
        channel_name = soup.find("span", itemprop="author").next.next['content']
        # channel URL
        channel_url = f"https://www.youtube.com/{channel_tag}"
        # number of subscribers as str
        channel_subscribers = videoSecondaryInfoRenderer[0]['owner']['videoOwnerRenderer']['subscriberCountText']['accessibility']['accessibilityData']['label']
        # store in the result dictionary
        result['channel'] = {'name': channel_name, 'url': channel_url, 'subscribers': channel_subscribers}
        # other channel features
        channel_details = f"https://www.youtube.com/{channel_name}/about"

        # getting video comments
        comments_list=[]

        try:
            accTag = soup.find_all("div", {"class":"content style-scope ytd-info-panel-content-renderer"})
            if(len(accTag) > 0):
                result['accreditationTag'] = 1
            else:
                result['accreditationTag'] = 0
        except:
            result['accreditationTag'] = 0
        # print(result['accreditationTag'])
        # print('selenium...')

        # with Chrome(executable_path=r'C:\Program Files\chromedriver.exe') as driver: on windows
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")
        with Chrome(options = options, executable_path = r'/usr/local/bin/chromedriver') as driver: # on mac
            wait = WebDriverWait(driver, 60) #15
            driver.get(video_url)

            for item in range(5): 
                print('loading..')
                wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
                time.sleep(1) #1
            try:
                for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content"))): 
                    c_unicode = comment.text.replace('\n', ' ')
                    c_encode = c_unicode.encode("ascii", "ignore")
                    c_decode = c_encode.decode()
                    comments_list.append(c_decode)
            except:
                print('Couldnt get video comments!')
            allComments = '****'.join(comments_list)
            result['comments'] = allComments
            
            driver.get(url = channel_details)
            allContent = driver.find_element_by_id("contents").text
            # description = driver.find_element_by_xpath("//div[@id='description']").text
            joinDate = driver.find_element_by_xpath(".//span[@class='style-scope yt-formatted-string'][2]").text
            # print(description)
            driver.close()
        
    except Exception as e:
        print('\n')
        print('\n')
        print('An exception occurred!')
        print('\n')
        print('\n')
        print(e)
    return result
