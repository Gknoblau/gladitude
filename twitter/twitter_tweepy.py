import datetime
import boto3
import tweepy
from geopy.geocoders import Nominatim
import json
from secret import *
import boto3
from textblob import TextBlob

# Get the service resource.
dynamodb = boto3.resource('dynamodb', )

table = dynamodb.Table('gladitude')



with open('../zip2fips.json') as data_file:
    zip2fips = json.load(data_file)


geolocator = Nominatim()
epoch = datetime.datetime.utcfromtimestamp(0)



def get_fips(coords):

    print(coords)
    location = geolocator.reverse('{:f}, {:f}'.format(coords[0], coords[1]))
    print(location.raw)
    if 'address' in location.raw:
        if 'country_code' in location.raw['address']:
            if location.raw['address']['country_code'] == 'us':
                if 'postcode' in location.raw['address']:
                    zipcode = location.raw['address']['postcode']
                else:
                    raise NoPostCode

                try:
                    fips = zip2fips[location.raw['address']['postcode']]
                except IndexError:
                    raise DNEInFips
                return fips, zipcode
            else:
                raise NotInUS


    else:
        raise NoAddressInRaw




class NoAddressInRaw(Exception):
    pass

class NoCountryCode(Exception):
    pass
class DNEInFips(Exception):
    pass

class NoPostCode(Exception):
    pass

class NotInUS(Exception):
    pass

class TwitterStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        try:
            if status.geo != None:

                fips, zipcode = get_fips(status.geo['coordinates'])
                testimonal = TextBlob(status.text)
                polarity = str(testimonal.sentiment.polarity)
                subjectivity = str(testimonal.sentiment.subjectivity)
                print(fips)
                print(zipcode)
                item_data = {
                    'ID': status.id,
                    'text': status.text,
                    'polarity': polarity,
                    'subjectivity': subjectivity,
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
