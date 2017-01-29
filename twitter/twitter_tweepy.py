import datetime
import tweepy
from geopy.geocoders import Nominatim
import json
from secret import *
import boto3
from textblob import TextBlob
import re
import preprocessor as p
p.set_options(p.OPT.URL, p.OPT.EMOJI)


# Get the service resource.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('fuck')
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
                print("Not in the US")
        else:
            print("No Country code is in the address")

    else:
        print("No address")



class TwitterStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            if status.geo != None:
                fips, zipcode = get_fips(status.geo['coordinates'])
                if fips is None:
                    print("Fips is None")
                    raise Exception
                if zipcode is None:
                    print("Zipcode is None")
                    raise Exception
                txt = re.sub('[!@#$]', '', status.text)
                txt = p.clean(txt)
                try:
                    table.update_item(
                        Key={
                            'fips': int(fips)
                        },
                        UpdateExpression='ADD tweet :val1',
                        ExpressionAttributeValues={
                            ':val1': set([txt])
                        }
                    )
                except:
                    print("it crashed")

                print("FIPS:" + fips)
                print("TXT:" + txt)

        except Exception as e:
            print(e)

    def on_error(self, status):
        print(status)

if __name__ == "__main__":
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # for i in range(4):
    #     t = threading.Thread(target=worker)
    #     t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
    #     t.start()
    stream = tweepy.Stream(auth, TwitterStreamListener())
    stream.filter(locations=[-125.0011, 24.9493, -66.9326, 49.5904])
        #stream.sample(1)
