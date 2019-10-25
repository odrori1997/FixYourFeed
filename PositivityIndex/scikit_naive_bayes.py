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

# Select the data we need
data = pd.read_csv('trainsent.csv', encoding='latin-1')
data = data[['Text', 'Sentiment']]
# data = data[ data.Sentiment != 2]

features = data['Text']
labels = data['Sentiment']

# Clean Tweets

def process(f):
	processed_features = []
	for tweet in range(0, len(f)):
		# print(tweet)
		# print(str(f[tweet]))
		processed_feature = re.sub(r'\W', ' ', str(f[tweet]))
		processed_feature = re.sub(r'\s+[a-zA-z]\s+', ' ', processed_feature)
		processed_feature = re.sub(r'\^[a-zA-z]\s+', ' ', processed_feature)
		processed_feature = re.sub(r'\s+', ' ', processed_feature, flags=re.I)
		processed_feature = re.sub(r'^b\s+', '', processed_feature)
		processed_feature = processed_feature.lower()
		processed_features.append(processed_feature)
	return processed_features


processed_features = process(features)


# print(processed_features[:10])

# Tfidf vectorizer
vectorizer = TfidfVectorizer(max_features=2500, min_df = 2, max_df = 0.8, stop_words = stopwords.words('english'))
processed_features = vectorizer.fit_transform(processed_features).toarray()

# split into testing and training sets
X_train, X_test, y_train, y_test = train_test_split(processed_features, labels, test_size=0.2, random_state = 0)

# Naive Bayes' classifier
model = GaussianNB()
model.fit(X_train, y_train)

# Test predictions

predictions = model.predict(X_test)
# print(X_test[:10])

# print(confusion_matrix(y_test,predictions))
print(classification_report(y_test,predictions))
print(accuracy_score(y_test, predictions))


# save model
f = open('my_classifier.pickle', 'wb')
pickle.dump(model, f)
f.close()

# temp = (data[ data.Sentiment == 1 ])

# Another test, custom tweets
sample = process([["i have hunger"], ["ugh hate everything"], ["blast"], ["darn"], ["happy"], ["happy said ugly to hog"], ["last tweet ha"]])
print(sample)
# sample = np.array(sample)
sample = vectorizer.fit_transform(sample).toarray()
# sample = sample.reshape(1, -1)
print(sample)
samplepred = model.predict(sample)
print(samplepred)


# TODO: implement neutral classification

# print(temp_words[0])
# pos_words = process(temp_words)
# neg_words = (data[ data.Sentiment == 0])
# neg_words = neg_words['Text']
# neg_words = process(neg_words)

# def pred(tweet):
# 	for t in tweet:
# 		text = t.split()

# 		val_pos = np.array([])
# 		val_neg = np.array([])
# 		for word in text:
# 			pos = pos_words.count(word)
# 			neg = neg_words.count(word)

# 			val_pos = np.append(val_pos, pos)
# 			val_neg = np.append(val_neg, neg)


# f = open('my_classifier.pickle', 'rb')
# classifier = pickle.load(f)
# f.close()
# sentiment_score = classifier.predict(tweet)

# print(sentiment_score)