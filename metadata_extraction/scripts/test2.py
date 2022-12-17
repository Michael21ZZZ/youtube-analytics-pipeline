import pandas as pd

def add_url(id):
    url_link = 'https://www.youtube.com/watch?v='
    return url_link + id

filter = pd.read_csv('./temp/filtered_four_per_keyword.csv')
filter['url'] = filter.apply(lambda row: add_url(row.id), axis = 1)
filter['url'].to_excel("url_list_new.xlsx")
#filter.to_excel('output.xlsx')
                     