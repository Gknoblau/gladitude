#Import the necessary methods from tweepy library
import tweepy
import pprint

#Variables that contains the user credentials to access Twitter API 
access_token = "825428485342507008-Sv7yaJk6pkFi8CNYQFHvCA5tPNcKb5S"
access_token_secret = "z45CtmlJoSgfgFrnqeDe41bxo0cUlpvdqzB3sQq0niIt5"
consumer_key = "eRoCZjX92AKa7GuJBR9VE0zqu"
consumer_secret = "oOJICZMxFS7p4ufXoIVQBMDpbz9tEWVTxGpW88WgyU8Mbndra6"

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
