from tweepy import API 
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
 
import twitter_credentials
import numpy as np
import pandas as pd
import re
import emojis


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
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth

# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()    

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_autenticator.authenticate_twitter_app() 
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(track=hash_tag_list)


# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
          
    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)


class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
    """
    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df

 
if __name__ == '__main__':

    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()

    api = twitter_client.get_twitter_client_api()

    #tweets = api.user_timeline(screen_name="hezesuibian", count=3)
    #tweepy.Cursor(api.search,q=search_words,count=50,lang="en",since=StartDate,till = EndDate, loc=search_loc,limit = limit,tweet_mode='extended').items():

    tweets = api.search(q = ["the","be","to","of","and","a"],lang="en",count = 200)

    print(dir(tweets[0]))
    print(tweets[0].retweet_count)
    print(tweets[0].coordinates)
    print(tweets[0].place)
    print("1111111")
    #print(emoji.demojize(tweets[0].text))

    #seee = tweets[0].text.encode("unicode_escape")
    #print(seee)
    #saww = seee.decode("unicode_escape")
    #print(saww)
    #swew = saww.encode("unicode_escape")
    #print(swew)

    #df = tweet_analyzer.tweets_to_data_frame(tweets)

    """
    print(dir(tweets[0].user))
    #print(df.head(10))
    for tweet in tweets:
        pass
        #print('1')
        
        #print(tweet.created_at)
        #print("1"+tweet.author.name)
        print(tweet.id)
        print(tweet.user.location)
        print("3"+tweet.author.screen_name)
        print("4"+tweet.lang)
        print(tweet.place)
        
        #print(tweet.favorite_count)

    """

    df = pd.DataFrame(columns=('id','date','author','location','likes','retweets','polarity','subjectivity','emoji_all','emoji_see','emoji_num','tweet'))
    for tweet in tweets:
        
        my_id = tweet.id
        date = tweet.created_at
        author = tweet.author.screen_name
        if tweet.place != None:
            location = tweet.place.name
        elif tweet.author.location != None:
            location = tweet.author.location
        else:
            location = tweet.user.location
        likes = tweet.favorite_count
        retweets = tweet.retweet_count
        

        clean_tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.text).split())
        analysis = TextBlob(clean_tweet)
        polarity = analysis.polarity
        subjectivity = analysis.subjectivity

        emoji_all = emojis.get(tweet.text)
        emoji_see = emojis.decode(str(emoji_all))
        emoji_num = emojis.count(tweet.text)

        tweet = tweet.text.encode("unicode_escape")



        s = pd.Series({'id':my_id,'date':date,'author':author,'location':location,'likes':likes,'retweets':retweets,'polarity':polarity,'subjectivity':subjectivity,'emoji_all':emoji_all,'emoji_see':emoji_see,'emoji_num':emoji_num,'tweet':tweet})
        df = df.append(s, ignore_index=True)
        

    df.to_csv('foo1.csv')
    

    #print(df.head(5))
    