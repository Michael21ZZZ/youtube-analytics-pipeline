from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession

def get_accreditation_tag(videoID):
    try:
        search_url = "https://www.youtube.com/watch?v="
        video_url = search_url + videoID
        # print('\n')
        print("Retrieving accTag for: ", video_url)
        # init an HTML Session
        session = HTMLSession()
        # get the html content
        response = session.get(video_url)
        response.html.render(scrolldown = 4, sleep=1, timeout=60)
        # create bs object to parse HTML
        soup = bs(response.html.html, "html.parser")
        acc_tag_text = soup.find_all("div", {"class":"content style-scope ytd-info-panel-content-renderer"})
        if(len(acc_tag_text) > 0):
            acc_tag = 1
        else:
            acc_tag = 0

    except:
        print('error in extracting accTag')
        acc_tag = 0

    return acc_tag

if __name__ == '__main__':
    videoID = "TgYY6cRazHM"
    print(get_accreditation_tag(videoID))



