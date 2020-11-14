from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
 
#import twitter_credentials
ACCESS_TOKEN = "1322032756126224384-qq3Vppy8tCebrdToefikIXlMfAQeuq"
ACCESS_TOKEN_SECRET = "oFmko6FXJi36XbkUAYxeafOxX595nOGMAeuUYBlIXN555"
CONSUMER_KEY = "PM43l0E6PPK2qNdeAmsKNEz7k"
CONSUMER_SECRET = "95phoJ00pRX0kXjFmndOlJrPBGHtwQhInNycpcDnOCRDnP50p0"


# # # # TWITTER STREAM LISTENER # # # #
class StdOutListener(StreamListener):
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
        print(status)

 
if __name__ == '__main__':
 
    # Authenticate using config.py and connect to Twitter Streaming API.
    my_hash_tag_list = ["donal trump"]
    my_fetched_tweets_filename = "tweets.txt"
    my_delimited = 1000
    my_language = ["en"]
    my_location = [-122.75,36.8,-121.75,37.8]

    listener = StdOutListener(my_fetched_tweets_filename)
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = Stream(auth, listener)

    # This line filter Twitter Streams to capture data by the keywords: 
    #stream.filter(track=my_hash_tag_list)
    a = stream.filter(locations = my_location)
    