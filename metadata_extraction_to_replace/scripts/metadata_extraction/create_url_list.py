import pandas as pd

def add_url(id):
    url_link = 'https://www.youtube.com/watch?v='
    return url_link + id

if __name__ == '__main__':
    final_data = pd.read_json('./output/final_data.json', lines = True)
    final_data['url'] = final_data.apply(lambda row: add_url(row.id), axis = 1)
    final_data['url'].to_excel("./output/video_url_list.xlsx", index = False)
