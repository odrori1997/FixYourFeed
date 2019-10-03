from django.utils import timezone
from django.db import models
from PositivityIndex.models import Twitter, Index
from django.contrib.auth.models import User
import numpy as np
import tweepy
import re
import matplotlib.pyplot as plt

from nltk.tokenize import WordPunctTokenizer
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from config import *

# Twitter api keys
# keysfile = open("../twitter_api_keys.txt", "r")
# keys = keysfile.readlines()
# API_KEY = keys[0].split()[2]
# API_SECRET_KEY = keys[1].split()[2]
# ACCESS_TOKEN = keys[2].split()[2]
# ACCESS_SECRET_TOKEN = keys[3].split()[2]

# connect to twitter api
def authentication(api_key, api_secret_key, access_token, access_secret_token):
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_secret_token)
    api = tweepy.API(auth)
    return api

# look at tweets from a given account
def search_tweets(user):
    api = authentication(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_SECRET_TOKEN)
    search_result = tweepy.Cursor(api.search, q=user, lang='en').items(10)

    try:
        tweet = search_result.next()
    except StopIteration:
        print("Error: Tweets not found.")

    return search_result

# return user's own timeline
def get_timeline(user):
    api = authentication(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_SECRET_TOKEN)
    search_result = tweepy.Cursor(api.user_timeline, id=user).items(10)

    print("--------------USER ---------------------")
    print(str(user))

    return search_result

# clean tweets for natural language processing
def clean_tweets(tweet):
    user_removed = re.sub(r'@[A-Za-z0-9]+','',tweet.decode('utf-8'))
    link_removed = re.sub('https?://[A-Za-z0-9./]+','',user_removed)
    number_removed = re.sub('[^a-zA-z]', ' ', link_removed)
    lower_case_tweet = number_removed.lower()
    tok = WordPunctTokenizer()
    words = tok.tokenize(lower_case_tweet)
    clean_tweet = (' '.join(words)).strip()
    return clean_tweet

# perform sentiment analysis on one tweet (Naive Bayesian Classifier)
def get_sentiment_score(tweet):
    client = language.LanguageServiceClient()
    document = types\
                    .Document(content=tweet,
                    type=enums.Document.Type.PLAIN_TEXT)
    sentiment_score = client\
                    .analyze_sentiment(document=document)\
                    .document_sentiment\
                    .score
    return sentiment_score

# analyze all tweets
def analyze_tweets(user, timeline):
    score = 0
    positive = 0
    neutral = 0
    negative = 0
    if timeline == True:
        tweets = get_timeline(user)
    else:
        tweets = search_tweets(user)
    for tweet in tweets:
        cleaned_tweet = clean_tweets(tweet.text.encode('utf-8'))
        # try:
        sentiment_score = get_sentiment_score(cleaned_tweet)
        # except InvalidArgument as e: # if tweet is in another language, continue
            # continue
        score += sentiment_score
        print('Tweet: {}'.format(cleaned_tweet))
        print('Score: {}'.format(sentiment_score))
        if sentiment_score <= -0.25:
            negative = negative+1
        elif sentiment_score <= 0.25:
            neutral = neutral+1
        else:
            positive = positive+1
    #final_score = round((score / float(positive+negative+neutral)), 2)
    final_score = score
    return (positive, neutral, negative, final_score)


def display_result(user, timeline):
    positive, neutral, negative, final_score = analyze_tweets(user, timeline)

    if final_score <= -0.25:
        status = 'NEGATIVE'
    elif final_score <= 0.25:
        status = 'NEUTRAL'
    else:
        status = 'POSITIVE'

    # modify database to add new index
    modifyDatabase(user, positive, negative, neutral, timeline)

#     # display message using matplotlib graphics
#     # labels = 'Positive', 'Neutral', 'Negative'
#     # sizes = [positive, neutral, negative]
#     # explode = (0.1, 0, 0)
#     # fig1, ax1 = plt.subplots()
#     # ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
#     #         shadow = True, startangle = 90)
#     # ax1.axis('equal')
#     # plt.show() # decide where to show this pie chart

def modifyDatabase(name, positive, negative, neutral, timeline):
    
    try:
        t = Twitter.objects.get(name=name)
    except Twitter.DoesNotExist:
        t = Twitter(name=name)
        t.save()
    if timeline == True:
        u = User.objects.get(username=name)
        i = Index(user=u, twitter=t, positive_tweets = positive, negative_tweets = negative,
                neutral_tweets = neutral, run_date = timezone.now())
    else:
        i = Index(twitter=t, positive_tweets = positive, negative_tweets = negative,
        neutral_tweets = neutral, run_date = timezone.now())
    i.save()
