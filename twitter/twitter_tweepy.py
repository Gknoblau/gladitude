#Import the necessary methods from tweepy library
import tweepy
import pprint

#Variables that contains the user credentials to access Twitter API 

class TwitterStreamListener(tweepy.StreamListener):
    def on_data(self, data):
        pprint.pprint(data)
        print()
        return True

    def on_error(self, status):
        print(status)

if __name__ == "__main__":
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = tweepy.Stream(auth, TwitterStreamListener())
    stream.sample()
