
import pandas as pd
import numpy as np 

import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import csv
import re # for regular expression
import string
import emoji

from collections import Counter 



def normalize_arabic(text):
    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("گ", "ك", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    return text


def remove_diacritics(text):
    diacritics = re.compile(""" ّ   | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)
    text = re.sub(diacritics, '', text)
    return text



def remove_repeating_char(text):
    return re.sub(r'(.)\1+', r'\1', text)




def remove_Eng_Char(text):


    text = ' '.join(re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)", " ", text).split())

    text = ' '.join(re.sub("(\w+:\/\/\S+)", " ", text).split())

    #remove english letters
    text= ' '.join(re.sub(r'[a-z]+'," ", text).split())
    text= ' '.join(re.sub('r[A-Z]+'," ", text).split())
    
    #remove numbers
    text = ''.join(i for i in text if not i.isdigit())
    
    return text



def remove_punctuations(text):
    text = ' '.join(re.sub("[\/\.\,\!\?\:\;\-\_\=؛\،\؟]", " ", text).split())
    return text





def preprocess_tweet(text):

    #Remove all the hashtags as hashtags do not affect sentiments in this case
    #Replace #word with word 
    text = ' '.join(re.sub(r'#([^\s]+)', r'\1', text).split())
    #text = ' '.join(re.sub((r"(?:\@|https?\://)\S+"), text).split())
    
    # remove diacritics from each word ot the text as it has alomost no impact on sentiments written in dialogue lang
    text= remove_diacritics(text)
    
    # normalize the tweet #working
    #check if the word in the dictionary list (it have two letters as part of the word)
    #text= normalize_arabic(text)
    
    # remove repeating charachters as they are common in dialogue lang
    text= remove_repeating_char(text)
    
    # remove English characters as the tweets are in arabic and this also include usernames mentions and URLs 
    text= remove_Eng_Char(text)
    
    # replace emojis and emoticons as they has a great impact on sentiments
    # note that should be done after removing any other undesired characters such as characters in English, usernames, hashtags, ...etc.
    # this is also should be performed before removing any punctiuation marks as people use them to express their emotions occasionally 
    
    # remove punctuations after convert emojis and emoticons to words
    text= remove_punctuations(text)
    
    return text



#read csv file 
file_name = pd.read_csv("Data.csv", encoding="utf-8")
nltk.download('punkt')



tweets = [] #empty list to store first column values
for i in range(0,  821):
    txt = preprocess_tweet(file_name['dialogue'][i])
    #text = nltk.word_tokenize(txt)  
    #pos = nltk.pos_tag(text)    
    tweets.append(txt)     
print(tweets)

dftweets = pd.DataFrame(tweets)


import csv

with open('DataClean.csv', "w", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        for ii in range(0, 821):
            writer.writerow([tweets[ii]])



    




