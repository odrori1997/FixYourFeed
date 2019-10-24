import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

import nltk
from nltk.corpus import stopwords
from nltk.classify import SklearnClassifier

# Select the data we need
data = pd.read_csv('trainsent.csv', encoding='latin-1')
data = data[['Text', 'Sentiment']]

# Split data into testing and training
train, test = train_test_split(data, test_size = 0.4)
train = train[train.Sentiment != 2]

train_pos = train[ train['Sentiment'] == 4]
train_pos = train_pos['Text']
train_neg = train[ train['Sentiment'] == 0]
train_neg = train_neg['Text']

tweets = []
stopwords_set = set(stopwords.words("english"))

for index, row in train.iterrows():
	words_filtered = [e.lower() for e in row.Text.split() if len(e) >= 3]
	words_cleaned = [word for word in words_filtered
	if 'http' not in word
	and not word.startswith('@')
	and not word.startswith('#')
	and word != 'RT']
	words_without_stopwords = [word for word in words_cleaned if not word in stopwords_set]
	tweets.append((words_without_stopwords, row.Sentiment))

test_pos = test[ test['Sentiment'] == 4]
test_pos = test_pos['Text']
test_neg = test[ test['Sentiment'] == 0]
test_neg = test_neg['Text']

def get_words_in_tweets(tweets):
	all = []
	for (words, sentiment) in tweets:
		all.extend(words)
	return all

def get_word_features(wordlist):
	wordlist = nltk.FreqDist(wordlist)
	features = wordlist.keys()
	return features
w_features = get_word_features(get_words_in_tweets(tweets))

def extract_features(document):
	document_words = set(document)
	features = {}
	for word in w_features:
		features['contains(%s)' % word] = (word in document_words)
	return features

# Training Naive Bayes classifier
training_set = nltk.classify.apply_features(extract_features, tweets)
classifier = nltk.NaiveBayesClassifier.train(training_set)

for obj in test_neg:
	print(obj.Text)
	res = classifier.classify(extract_features(obj.split()))
	if(res == 'Negative'):
		neg_cnt = neg_cnt + 1
for obj in test_pos:
	print(obj.Text)
	res = classifier.classify(extract_features(obj.split()))
	if (res == 'Positive'):
		pos_cnt = pos_cnt + 1

print('[Negative]: %s/%s' % (len(test_neg), neg_cnt))
print('[Positive]: %s/%s' % (len(test_pos), pos_cnt))