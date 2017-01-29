import datetime
import tweepy
from geopy.geocoders import Nominatim
import json
from secret import *
import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb', )
table = dynamodb.Table('gladitude')
geolocator = Nominatim()
epoch = datetime.datetime.utcfromtimestamp(0)

with open('../zip2fips.json') as data_file:
    zip2fips = json.load(data_file)


def get_fips(coords):
    location = geolocator.reverse('{:f}, {:f}'.format(coords[0], coords[1]))
    zipcode = None
    fips = None

    if 'address' in location.raw:
        if 'country_code' in location.raw['address']:
            if location.raw['address']['country_code'] == 'us':
                if 'postcode' in location.raw['address']:
                    zipcode = location.raw['address']['postcode']
                else:
                    print("postcode not in location address")

                try:
                    fips = zip2fips[location.raw['address']['postcode']]
                except IndexError:
                    print("FIPS could not be found")

                return fips, zipcode
            else:
                print()
        else:
            pass

    else:
        raise NoAddressInRaw



class TwitterStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        try:
            if status.geo != None:
                fips, zipcode = get_fips(status.geo['coordinates'])
                print(fips)
                print(zipcode)
                item_data = {
                    'ID': status.id,
                    'text': status.text,
                    'timestamp': int((status.created_at - epoch).total_seconds() * 1000),
                    'fips': int(fips),
                    'zipcode': int(zipcode),
                    'hashtags': status.entities['hashtags']
                }
                import pprint; pprint.pprint(item_data)
                print("putting data in")
                table.put_item(Item=item_data)

        except Exception as e:
            print(e)


    def on_error(self, status):
        print(status)

if __name__ == "__main__":
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = tweepy.Stream(auth, TwitterStreamListener())
    stream.sample(1)
