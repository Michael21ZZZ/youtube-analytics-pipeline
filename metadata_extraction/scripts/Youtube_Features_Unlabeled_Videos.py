import json
import pprint
import nltk
#nltk.download()
from io import open
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import sys
from datetime import date
import datetime
import readability 
from collections import Counter
from nltk.tokenize import TweetTokenizer
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import pandas as pd
import os 

# open the query result
summary = ["finally", "in a word", "in brief", "briefly", "in conclusion", "in the end", "in the final analysis", "on the whole", "to conclude", "to summarize", "in sum", "to sum up", "in summary", "lastly"]
transition = ["accordingly", "as a result", "and so", "because", "consequently", "for that reason", "hence", "on account of", "since", "therefore", "thus", "after", "afterwards", "always", "at length", "during", "earlier", "following", "immediately", "in the meantime", "later", "never", "next", "once", "simultaneously", "so far", "sometimes", "soon", "subsequently", "then", "this time", "until now", "when", "whenever", "while", "additionally", "again", "also", "and", "or", "not", "besides", "even more", "finally", "first", "firstly", "further", "furthermore", "in addition", "in the first place", "in the second place", "last", "lastly", "moreover", "next", "second", "secondly", "after all", "although", "and yet", "at the same time", "but", "despite", "however", "in contrast", "nevertheless", "notwithstanding", "on the contrary", "on the other hand", "otherwise", "thought", "yet", "as an illustration", "e.g.", "for example", "for instance", "specifically", "to demonstrate", "to illustrate", "briefly", "critically", "foundationally", "more importantly", "of less importance", "primarily", "above", "centrally", "opposite to", "adjacent to", "below", "peripherally", "nearby", "beyond", "in similar fashion", "in the same way", "likewise", "in like manner", "i.e.", "in other word", "that is", "to clarify", "to explain", "in fact", "of course", "undoubtedly", "without doubt", "surely", "indeed", "for this purpose", "so that", "to this end", "in order that", "to that end"]

f=open('./complete_data.txt', encoding='utf-8')
sid=SentimentIntensityAnalyzer()
tknzr = TweetTokenizer()
lines=f.readlines()

# to be used to add features from each video, a list of dictionaries
dict_list = []

for line in lines: 
	line=line.encode('ascii', 'ignore').decode('utf-8')
	video=json.loads(line)
	features={}
	print(video['id'])
	#id
	features['id']=video['id']
	#has title
	if len(video['title'])>0:
		features['has_title']=1
	else:
		features['has_title']=0
	#has description 
	if len(video['description'])>0:
		features['has_description']=1
	else:
		features['has_description']=0
	#has tags
	if len(video.get('tags',""))>0:
		features['has_tags']=1
	else:
		features['has_tags']=0
	# cosine similarity
	features ['cosine_similarity']=video['cosine_similarity']
	#accreditation tag
	if 'accreditationTag' in video.keys():
		if video['accreditationTag'] == 1:
			features['accredited']=1
		else:
			features['accredited']=0
	else:
		features['accredited']=0

	transition_words = 0
	summary_words = 0
	active_verb=0
	features['readability']=0
	features['sentence_count']=0
	features['word_count']=0
	features['word_unique']=0
	#readability
	video['description'] = re.sub(r'^https?:\/\/.*[\r\n]*', '', video['description'], flags=re.MULTILINE)
	text= sent_tokenize(video['description'])
	if len(text)>0:
		try:
			results = readability.getmeasures(text, lang='en')
			features['readability']= results['readability grades']['ARI']
	#Sentence count 
			features['sentence_count']=results['sentence info']['sentences']
	#Word count
			features['word_count']=results['sentence info']['words']
	#unique word count
			features['word_unique']=results['sentence info']['wordtypes']
	#active verb 
			tokens=word_tokenize(video['description'].lower())
			tags = nltk.pos_tag(tokens)
			counts = Counter( tag for word,  tag in tags)
			active_verb = counts.get("VB",0)+counts.get("VBD",0)+counts.get("VBG",0)+counts.get("VBP",0)+counts.get("VBZ",0)
	#summary words
			for i in summary:
				if i in video['description']:
					summary_words+=1
	# transition words
			for i in transition:
				if i in video['description']:
					transition_words+=1
		except ValueError:
			print("Decription not Found")

	features['transition_words']=transition_words
	features['summary_words']=summary_words
	features['active_verb']=active_verb
	#Perceived time
	features['duration']=video['duration']
	dict_list.append(features)

# writing features for each video (dictionary) into a csv file
lst = []
for dictionary in dict_list:
	lst.append(pd.json_normalize(dictionary))

all_features_df = pd.concat(lst, axis=0).fillna(0)
all_features_df = all_features_df.drop_duplicates(subset='id', keep='first')
all_features_df.to_csv('features_unlabeled_videos.csv', index = False)

	
