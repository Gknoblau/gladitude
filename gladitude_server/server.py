from flask import Flask
import boto3
import json
app = Flask(__name__)


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('gladitude')


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
    return json.dumps(RESULT)

if __name__ == "__main__":
    app.run()