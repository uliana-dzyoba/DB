import tweepy as tw
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import nltk
from nltk.corpus import stopwords
from textblob import Word, TextBlob
from pymongo import MongoClient

# API keys and tokens
consumer_key = 'tm3OeqivBX8CQO0jKk2vI2tPv'
consumer_secret = 'dQNVeceowO0pRsufU6aghodUoV8ywPKjjxA10viYG3wOY9Bc0R'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAC8NQAEAAAAAiMedzobgmMJgCWs7YTCydTAMYkQ%3D00FSTb1ero3K8IRzzxMl6MRcXvdOug2jjm9K2qiiwjsVQITCHB'
access_token = '4581746128-N1ZrI32cZFy4R2sOwXDNm601YGzLLOxjjhMnyNO'
access_token_secret = '3j6eWmzEyMYd7ppbEa98YERfGvQmYiGS5tp8iex2TrZDH'

# Authorization
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# Remote database
cluster = MongoClient("mongodb+srv://test:tset1@cluster0.d1qza.mongodb.net/twitter?retryWrites=true&w=majority")
db_remote = cluster.twitter
collection = db_remote.tweets

# Database
client = MongoClient('mongodb://localhost:27017/')
db = client.tweepy
#collection = db.tweets

#Replica set
c = MongoClient('mongodb://localhost:40001,localhost:40002,localhost:40003,localhost:40004,localhost:40005,localhost:40006')
rs = c.tweepy
#collection = rs.tweets

# nltk.download('stopwords')
# nltk.download('wordnet')


def preprocess_tweets(tweet, custom_stopwords):
    stop_words = stopwords.words('english')
    preprocessed_tweet = tweet
    preprocessed_tweet.replace('[^\w\s]', '')
    preprocessed_tweet = " ".join(word for word in preprocessed_tweet.split() if word not in stop_words)
    preprocessed_tweet = " ".join(word for word in preprocessed_tweet.split() if word not in custom_stopwords)
    preprocessed_tweet = " ".join(Word(word).lemmatize() for word in preprocessed_tweet.split())
    return preprocessed_tweet

def preprocess_df(df, custom_stopwords):
    df['Processed Tweet'] = df['Tweets'].apply(lambda x: preprocess_tweets(x, custom_stopwords))
    df.drop(columns='Tweets')
    return df

def get_polarity_subjectivity(df):
    df['polarity'] = df['Processed Tweet'].apply(lambda x: TextBlob(x).sentiment[0])
    df['subjectivity'] = df['Processed Tweet'].apply(lambda x: TextBlob(x).sentiment[1])
    return df

def chart_polarity(df):
    rows = len(df.index)
    positive = float(sum(df['polarity'] > 0)) / float(rows) * 100
    negative = float(sum(df['polarity'] < 0)) / float(rows) * 100
    neutral = float(sum(df['polarity'] == 0)) / float(rows) * 100
    labels = 'Positive', 'Neutral', 'Negative'
    sizes = [positive, neutral, negative]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')
    ax1.set_title("\n".join(['Polarity distribution']))
    plt.savefig('chart.png', bbox_inches='tight')

def table_polarity_subjectivity(df):
    table = df[['polarity', 'subjectivity']].agg([np.mean, np.max, np.min, np.median])
    print(table)
    f = open("table.txt", "w")
    f.write(table.to_string())
    f.close()

def plot_ma_polarity(df):
    sub = df[['Timestamp', 'polarity']]
    sub = sub.sort_values(by='Timestamp', ascending=True)
    sub['MA Polarity'] = sub.polarity.rolling(10, min_periods=3).mean()
    fig, ax = plt.subplots(figsize=(13, 10))
    ax.plot(sub['Timestamp'], sub['MA Polarity'])
    ax.set_title("\n".join(['Moving Average Polarity']))
    plt.savefig('graph.png', bbox_inches='tight')

def get_tweets_by_hashtag_or_keyword(hashtag_or_keyword):
    query = tw.Cursor(api.search, q=hashtag_or_keyword, lang='en').items(10000)
    tweets = [{'Tweets': tweet.text, 'Timestamp': tweet.created_at} for tweet in query]
    collection.insert_many(tweets)

def get_tweets_df_from_db():
    tweets = collection.find()
    return pd.DataFrame.from_dict(tweets)

def get_trending():
    woeid = 23424977
    trends = api.trends_place(woeid)
    results = trends[0]["trends"]
    for trend in results:
        print(trend["name"])

def preprocess():
    df = get_tweets_df_from_db()
    custom_stopwords = ['RT', hashtag]
    df = preprocess_df(df, custom_stopwords)
    df = get_polarity_subjectivity(df)
    return df

def show_menu():
    print("[1] View trends")
    print("[2] Load tweets")
    print("[3] Polarity statistics table")
    print("[4] Polarity chart")
    print("[5] MA Polarity graph")
    print("[0] Exit")
    print()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # collection.delete_many({})
    hashtag = '#corpsehoodie'
    show_menu()
    option = int(input('Enter option: '))
    while option != 0:
        if option == 1:
            get_trending()
        elif option == 2:
            hashtag = input('Enter hashtag: ')
            get_tweets_by_hashtag_or_keyword(hashtag)
        elif option == 3:
            df = preprocess()
            table_polarity_subjectivity(df)
        elif option == 4:
            df = preprocess()
            chart_polarity(df)
        elif option == 5:
            df = preprocess()
            plot_ma_polarity(df)
        else:
            print("invalid option")
        print()
        show_menu()
        option = int(input('Enter option: '))
