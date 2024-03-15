import numpy
import pandas
import nltk
import json
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))
raw_text_document = open('plaintext.txt', 'r', encoding="utf-8")
raw_text_content = raw_text_document.read()
tokenized_text = [nltk.pos_tag(word_tokenize(
    t)) for t in sent_tokenize(raw_text_content)]
all_words = []
for sentence in tokenized_text:
    for word in sentence:
        all_words.append(word[0])
freqancy = nltk.FreqDist(all_words)
print(freqancy)
dict_of_content = dict()
for sentence in tokenized_text:
    for word in sentence:
        dict_of_content[word[0]] = [lemmatizer.lemmatize(
            word[0]), word[1], freqancy[word[0]]]


# DataDict = raw_text_document.read()
# DataDict = nltk.FreqDist(nltk.tokenize.word_tokenize(DataDict))
# elem_list = []
# for key in DataDict.keys():
#    if (key in stop_words) or len(key) > 20 or len(key) < 3:
#        elem_list.append(key)
# for key in elem_list:
#    DataDict.pop(key)
json_document = open('corpus.json', 'w+', encoding="utf-8")
json.dump(dict_of_content, json_document, indent=4, ensure_ascii=False)
json_document.close()
raw_text_document.close()
