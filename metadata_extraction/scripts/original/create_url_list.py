import pandas as pd

def add_url(id):
    url_link = 'https://www.youtube.com/watch?v='
    return url_link + id

final_data = pd.read_json('final_data.json')
final_data['url'] = final_data.apply(lambda row: add_url(row.id), axis = 1)
final_data['url'].to_excel("url_list.xlsx")
