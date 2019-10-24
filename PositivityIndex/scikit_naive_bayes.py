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
processed_features = []

# Clean Tweets

for tweet in range(0, len(features)):
	processed_feature = re.sub(r'\W', ' ', str(features[tweet]))
	processed_feature = re.sub(r'\s+[a-zA-z]\s+', ' ', processed_feature)
	processed_feature = re.sub(r'\^[a-zA-z]\s+', ' ', processed_feature)
	processed_feature = re.sub(r'\s+', ' ', processed_feature, flags=re.I)
	processed_feature = re.sub(r'^b\s+', '', processed_feature)
	processed_feature = processed_feature.lower()
	processed_features.append(processed_feature)


print(processed_features)
# Tfidf vectorizer
vectorizer = TfidfVectorizer(max_features=2500, min_df = 7, max_df = 0.8, stop_words = stopwords.words('english'))
processed_features = vectorizer.fit_transform(processed_features).toarray()

print(processed_features)

# split into testing and training sets
X_train, X_test, y_train, y_test = train_test_split(processed_features, labels, test_size=0.2, random_state = 0)

# Naive Bayes' classifier
model = GaussianNB()
model.fit(X_train, y_train)

# Test predictions

predictions = model.predict(X_test)
print(X_test)[:10]

# print(confusion_matrix(y_test,predictions))
print(classification_report(y_test,predictions))
print(accuracy_score(y_test, predictions))

f = open('my_classifier.pickle', 'wb')
pickle.dump(model, f)
f.close()

# for word in processed_features:



# tweet = "mean hate ugh"
# tweet = tweet.split()
# tweet = [["mean"]]

# f = open('my_classifier.pickle', 'rb')
# classifier = pickle.load(f)
# f.close()
# sentiment_score = classifier.predict(tweet)

# print(tweet)
# print(sentiment_score)