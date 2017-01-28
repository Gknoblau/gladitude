#Import the necessary methods from tweepy library
import datetime

import boto.dynamodb
import tweepy

#Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = "825428485342507008-Sv7yaJk6pkFi8CNYQFHvCA5tPNcKb5S"
ACCESS_TOKEN_SECRET = "z45CtmlJoSgfgFrnqeDe41bxo0cUlpvdqzB3sQq0niIt5"
CONSUMER_KEY = "eRoCZjX92AKa7GuJBR9VE0zqu"
CONSUMER_SECRET = "oOJICZMxFS7p4ufXoIVQBMDpbz9tEWVTxGpW88WgyU8Mbndra6"

epoch = datetime.datetime.utcfromtimestamp(0)
conn = boto.dynamodb.connect_to_region(
        'us-west-2',
        aws_access_key_id='AKIAIIMMXJREASSBQ6ZA',
        aws_secret_access_key='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')

table = conn.get_table('tweets')

class TwitterStreamListener(tweepy.StreamListener):

    def on_status(self, status):

        if status.geo != None:
            item_data = {
                'id': status.id,
                'text': status.text,
                'timestamp': (status.created_at - epoch).total_seconds() * 1000.0,
                'coordinates': status.coordinates,
                'hashtags': status.entities['hashtags'],
                'location': status.coordinates
            }
            print(status.coordinates)

    def on_error(self, status):
        print(status)


class Tweet():

    def __init__(self):
        pass

if __name__ == "__main__":
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = tweepy.Stream(auth, TwitterStreamListener())
    stream.sample(1)

