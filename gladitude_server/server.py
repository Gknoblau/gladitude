from flask import Flask

import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
from textblob import TextBlob
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources=r'*', crossdomain=True)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('fuck')
print(table)


with open('../zip2fips.json') as data_file:
    zip2fips = json.load(data_file)

fips = set(zip2fips.values())


@app.route("/")
def hello():
    resp = table.scan(FilterExpression=Attr("fips").exists())
    sorted_by_fips = {}
    sorted_by_fips['items'] = []
    for item in resp['Items']:
        concat = " ".join(item['tweet'])
        testimonal = TextBlob(concat)
        polarity = (testimonal.sentiment.polarity)

        sorted_by_fips['items'].append({'id':str(item['fips']), 'rate': polarity})

    return json.dumps(sorted_by_fips)

if __name__ == "__main__":
    app.run()