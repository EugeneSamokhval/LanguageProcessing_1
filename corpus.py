import numpy
import pandas
import nltk
import json
from nltk.corpus import stopwords

stop_words = set(stopwords.words("english"))
raw_text_document = open('plaintext.txt', 'r', encoding="utf-8")
DataDict = raw_text_document.read()
DataDict = nltk.FreqDist(nltk.tokenize.word_tokenize(DataDict))
elem_list = []
for key in DataDict.keys():
    if (key in stop_words) or len(key) > 20 or len(key) < 3:
        elem_list.append(key)
for key in elem_list:
    DataDict.pop(key)
json_document = open('corpus.json', 'w+', encoding="utf-8")
json.dump(DataDict, json_document, indent=4, ensure_ascii=False)
json_document.close()
raw_text_document.close()
