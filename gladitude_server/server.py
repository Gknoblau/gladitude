from flask import Flask

import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
from textblob import TextBlob
import preprocessor as p

app = Flask(__name__)


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('fuck')
print(table)


with open('../zip2fips.json') as data_file:
    zip2fips = json.load(data_file)

fips = set(zip2fips.values())

RESULT = {'ID': 825535001265655808,
          'fips': 34035,
          'hashtags': [],
          'polarity': '0.5',
          'subjectivity': '0.5',
          'text': "@ScottPresler Most people would be ok with that, but that's not what "
                  "happened, is it? Fools didn't think it thru all the way, or set it "
                  'up.',
          'timestamp': 1485657856000,
          'zipcode': 8873}

@app.route("/")
def hello():
    resp = table.scan(FilterExpression=Attr("fips").exists())
    sorted_by_fips = {}
    for item in resp['Items']:
        concat = " ".join(item['tweet'])
        testimonal = TextBlob(concat)
        polarity = (testimonal.sentiment.polarity)

        sorted_by_fips[str(item['fips'])] = polarity

    return json.dumps(sorted_by_fips)



if __name__ == "__main__":
    app.run()