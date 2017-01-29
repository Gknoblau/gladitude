import datetime
import boto.dynamodb
import tweepy
from geopy.geocoders import Nominatim
import usaddress
import json

from secret import *


# SETUP
geolocator = Nominatim()
epoch = datetime.datetime.utcfromtimestamp(0)

conn = boto.dynamodb.connect_to_region(
        'us-west-2',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key)
# table = conn.get_table('tweets')

with open('zip2fips.json') as data_file:
    zip2fips = json.load(data_file)


def get_fips(coords):
    print(type(coords[0]))
    location = geolocator.reverse('{:f}, {:f}'.format(coords[0], coords[1]))
    print(type(location.address))
    d = usaddress.tag(location.address)
    if 'AddressNumber' not in d[0].keys():
        raise ZipCodeException()
    else:

        return zip2fips[d[0]['AddressNumber']]


class ZipCodeException(Exception):
    pass


class TwitterStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        try:
            if status.geo != None:
                print(status.coordinates['coordinates'])
                print(status.geo)
                item_data = {
                    'id': status.id,
                    'text': status.text,
                    'timestamp': (status.created_at - epoch).total_seconds() * 1000.0,
                    'coordinates': status.coordinates['coordinates'],
                    'fips': get_fips(status.geo['coordinates']),
                    'hashtags': status.entities['hashtags'],
                    'location': status.coordinates
                }
                import pprint; pprint.pprint(item_data)

        except ZipCodeException:
            print("Zip code error - skipping this tweet")
        except KeyError:
            print('zip code dne on zip2fips')

    def on_error(self, status):
        print(status)

if __name__ == "__main__":
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = tweepy.Stream(auth, TwitterStreamListener())
    stream.sample(1)
