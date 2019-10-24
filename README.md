# FixYourFeed

A website that measures a Twitter user's Positivity Index. 
Sentiment Analysis is performed on the tweets in a given user's Timeline. A graph is shown of the user's Timeline with % Positive & % Negative Tweets. 

There are two available ML models for use:
  -One is available through the Google Cloud NLP API. 
  -The second I created, at /PositivityIndex/scikit_naive_bayes. It was trained on a Kaggle dataset, provided in /PositivityIndex/trainsent.csv. Measured accuracy was 71% using Gaussian Naive Bayes Classifier.

Twitter & Google Cloud API keys not provided for privacy reasons. 
