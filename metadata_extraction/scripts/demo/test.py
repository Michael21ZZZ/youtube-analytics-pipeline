import pandas as pd
trial = pd.read_csv('trial.csv')
a = trial.groupby('keyword').apply(lambda s: s.sample(min(len(s), 4)))
b = a.loc[:,['keyword','id','rank']]
b.to_csv('./temp/filtered_four_per_keyword.csv', index=False)
#print(b)