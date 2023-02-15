'''
Returns a list of 100 keywords which is ranked based on popularity on Google trends.

@params: path for list of original keywords in .csv file
'''

import pandas
import pytrends
from pytrends.request import TrendReq
import pandas as pd
import time
import sys
import os
import shutil
import glob
import openpyxl

pytrends = TrendReq(geo='US', tz=360)
MAX_COMPARE_NUM = 5

# creates 5-word lists and compares the relative popularity of each word within it
def gtrends_overtime(kw_list, key_ref, save_name="", directory = "", category=0, time='all', loc=''):
    #iterate every 4 item in list plus a keyword reference as the relative comparison
    i = 0
    while i < len(kw_list):
        l = kw_list[i:(i+4)]
        l.append(key_ref)
        pytrends.build_payload(l, cat=category, timeframe=time, geo=loc, gprop='')
        df_time = pytrends.interest_over_time()
        df_time.reset_index(inplace=True)
        df_time_name = "gtrends_overtime"+str(save_name)+str((i+4)//4)+".csv"
        df_time.to_csv(os.path.join(directory, df_time_name), index = False)
        i += 4

# combining all the csv files (each file containing 4 words + the key word)
def combine_wbase(directory, base_name, n_file, filename):
    df1 = pd.read_csv(directory+base_name+str(1)+".csv")
    for i in range(n_file-1):
        df2 = pd.read_csv(directory+base_name+str(i+2)+".csv")
        df1 = pd.concat([df1, df2], axis=1, sort=False)
    df_name = filename
    # Saving the merged file 
    df1.to_csv(df_name, index = False)

# Tidy up IsPartial column for data overtime
def partial(df, n_file):
    for i in range(n_file-1):
        df = df.drop(columns="isPartial."+str(i+1)+"")
    if df.isPartial.tail(1).bool() == True:
        df = df.drop(df.isPartial.tail(1).index, axis=0)
    df = df.drop(columns="isPartial")
    return df

def normalise(df, n_file, key_ref, col='date'):
    li = []
    # Checking the relative popularity between comparisons
    for i in range(n_file-1):    
        df = df.drop(columns=col+"."+str(i+1)+"")
        # Appending the list if relative popularity of the keyword reference is different
        if df[key_ref+"."+str(i+1)+""][0] == df[key_ref][0]:
            pass
        else:
            li.append(i+1)
    
    # Normalizing relative popularity when the relative popularity of the keyword reference is different         
    for l in li:
        k = df.columns.get_loc(key_ref+"."+str(l)+"")
        for n in range(len(df.index)):
            # Computing relative popularity by normalizing according to the reference
            if df.iloc[n,(k)] > 0:
                for m in range(5):
                    df.iloc[n,(k-4+m)] = (df.iloc[n,(k-4+m)] * (df[key_ref][n]/df.iloc[n,(k)]))
            else:
                for m in range(5):
                    df.iloc[n,(k-4+m)] = (df.iloc[n,(k-4+m)] * (df[key_ref][n]/0.01))
    return df

def get_trends(keyword_path, keyword_ref, num_result):
    '''
    Returns a list of 100 keywords which is ranked based on popularity on Google trends.

    @params: keyword_path, path for list of original keywords in .csv file. No header for this file.
    @oarams: keyword_ref, reference keyword for popularity comparison. Should be set manually. 
    @params: num_results, number of keywords expected in the final list
    
    '''
    keyword_file = pd.read_csv(keyword_path, header=None) # Modified for different disease, Input the keyword list
    # InputList should have 228 keywords (to do: input file should not contain ref keyword) It should be 229??
    kw_list = keyword_file.iloc[:,0].values.tolist()
    path = "./googletrends"
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path) 
    num_iteration = len(kw_list) // (MAX_COMPARE_NUM - 1) + 1 # num for iteration
    # trends of words within each list of five keywords, using diabetes causes as the reference keyword
    gtrends_overtime(kw_list, keyword_ref, "_worldwide_", directory = './googletrends', category=0, time='today 5-y', loc='US')
    # combining all 57 data files wtihin the google trends folder
    combined = combine_wbase("./googletrends/", "gtrends_overtime_worldwide_", num_iteration - 1, "./googletrends/gtrends_overtime_worlwide_merged.csv")
    # reading the combined csv file back into a pandas df
    combined = pd.read_csv("./googletrends/gtrends_overtime_worlwide_merged.csv")
    # removing the ISPARTIAL column from the dataframes
    combined = partial(combined, num_iteration - 1)
    # normalizing the combined dataframe to get relative popularity of all keywords
    normalised = normalise(combined, n_file = num_iteration - 1, key_ref = keyword_ref, col='date')
    # remove repititive columns for reference keyword being concatenated above in all the files
    for i in range(num_iteration - 2):    
        normalised = normalised.drop(columns = keyword_ref+"."+str(i+1)+"")
    # finding the average relative popularity of each keyword in the list of 228 keywords + ref_keyword 
    avg_popularity = normalised.mean().sort_values(ascending = False).head(num_result)   
    final_keyword_list = avg_popularity.index.to_list()
    # remove temporary google trends file
    if os.path.exists(path):
        shutil.rmtree(path)
        
    return final_keyword_list

if __name__ == '__main__':
    keyword_path = './input/input_keyword_list.csv' # Modified for different disease, Input the keyword list
    keyword_ref = 'sleep apnea causes' # use the first keyword for comparison in each iteration. 
    num_of_result = 100
    keyword_list = get_trends(keyword_path, keyword_ref, num_of_result)
    print(keyword_list[:10])