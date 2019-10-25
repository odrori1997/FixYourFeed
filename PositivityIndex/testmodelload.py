import numpy as np
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

import nltk
from nltk.corpus import stopwords

import pickle

import scikit_naive_bayes as sknb


f = open('my_classifier.pickle', 'rb')
classifier = pickle.load(f)
f.close()

def analyzeTweet(tweet):
	data = sknb.process(tweet)
	vectorizer = TfidfVectorizer(max_features=2500, min_df = 2, max_df = 0.8, stop_words = stopwords.words('english'))
	data = vectorizer.fit_transform(data).toarray()
	sentiment_score = classifier.predict(tweet)
	return sentiment_score

# print(tweet)
# print(sentiment_score)