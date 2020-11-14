from tweepy import API 
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
import numpy as np
import pandas as pd
import re
import emojis
import time
import cv2
import _thread


# # # # import twitter_credentials
ACCESS_TOKEN = "1322032756126224384-qq3Vppy8tCebrdToefikIXlMfAQeuq"
ACCESS_TOKEN_SECRET = "oFmko6FXJi36XbkUAYxeafOxX595nOGMAeuUYBlIXN555"
CONSUMER_KEY = "PM43l0E6PPK2qNdeAmsKNEz7k"
CONSUMER_SECRET = "95phoJ00pRX0kXjFmndOlJrPBGHtwQhInNycpcDnOCRDnP50p0"

# # # # TWITTER CLIENT # # # #
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

    def get_search(self, num_tweets):
        search_words = ["a","e","i","o","u"]
        seach_result = []
        for tweet in Cursor(self.twitter_client.search,q=search_words,lang="en").items(num_tweets):
            seach_result.append(tweets)
        return seach_result


# # # # TWITTER AUTHENTICATER # # # #
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        return auth


# # # # MAIN # # # #

def input_thread(a_list):
    input()
    a_list.append(True)



if __name__ == '__main__':

    wordlist = []
    for line in open("word.txt"): 
        wordlist.append(line.replace('\n','')) 


    twitter_client = TwitterClient()

    api = twitter_client.get_twitter_client_api()

    #tweets = api.user_timeline(screen_name="hezesuibian", count=3)
    #tweepy.Cursor(api.search,q=search_words,count=50,lang="en",since=StartDate,till = EndDate, loc=search_loc,limit = limit,tweet_mode='extended').items():

    df = pd.DataFrame(columns=('id','date','author','location','likes','retweets','polarity','subjectivity','emoji_all','emoji_see','emoji_num','tweet'))
    
    a_list = []
    id_list = []
    _thread.start_new_thread(input_thread, (a_list,))

    while not a_list:
        
        for i in range(100):

            #Set the search keywords are most common English words, it should be the almost every tweets. 
            #I think we can only get 100 tweets once.
            keywords = wordlist[i*10 : i*10+10]
            print(keywords)
            #tweets = api.search(q = str(keywords),lang="en",count = 100)
            for tweet in Cursor(api.search,q=keywords,lang="en").items(1000):
            #print(tweets)

            #for tweet in tweets:

                #if (emojis.count(tweet.text) != 0)  and (tweet.id not in id_list):
                if  (tweet.id not in id_list):
                    #basic information of tweets
                    my_id = tweet.id
                    #print(id_list)
                    id_list.append(tweet.id)
                    date = tweet.created_at
                    author = tweet.author.screen_name
                    #many tweets don't have location information
                    if tweet.place != None:
                        location = tweet.place.name
                    elif tweet.author.location != None:
                        location = tweet.author.location
                    else:
                        location = tweet.user.location
                    likes = tweet.favorite_count
                    retweets = tweet.retweet_count
                    
                    #use TextBlob to do sentiment analysis
                    clean_tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.text).split())
                    analysis = TextBlob(clean_tweet)
                    polarity = analysis.polarity
                    subjectivity = analysis.subjectivity


                    #use emojis to do emoji process
                    emoji_all = emojis.get(tweet.text)
                    emoji_see = emojis.decode(" ".join(emoji_all))
                    emoji_num = emojis.count(tweet.text)

                    #previous tweet text data, use unicode to encode, also can .decode("unicode_escape") 
                    tweet = tweet.text.encode("unicode_escape")

                    s = pd.Series({'id':my_id,'date':date,'author':author,'location':location,'likes':likes,'retweets':retweets,'polarity':polarity,'subjectivity':subjectivity,'emoji_all':emoji_all,'emoji_see':emoji_see,'emoji_num':emoji_num,'tweet':tweet})
                    df = df.append(s, ignore_index=True)

            print(df.shape[0])
            print(i)
            time.sleep(3)



    
    df.to_excel('TweetData_emoji.xlsx', sheet_name='Sheet1')  # Excel is better, beecause we can see the emoji

        
    