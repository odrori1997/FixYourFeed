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

tweet = [["mean"]]

f = open('my_classifier.pickle', 'rb')
classifier = pickle.load(f)
f.close()
sentiment_score = classifier.predict(tweet)

print(tweet)
print(sentiment_score)