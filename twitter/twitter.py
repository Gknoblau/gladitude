import twitter

CONSUMER_KEY = 'eRoCZjX92AKa7GuJBR9VE0zqu'
CONSUMER_SECRET = 'oOJICZMxFS7p4ufXoIVQBMDpbz9tEWVTxGpW88WgyU8Mbndra6'
ACCESS_TOKEN = '825428485342507008-Sv7yaJk6pkFi8CNYQFHvCA5tPNcKb5S'
ACCESS_TOKEN_SECRET ='z45CtmlJoSgfgFrnqeDe41bxo0cUlpvdqzB3sQq0niIt5'

api = twitter.Api(consumer_key=[CONSUMER_KEY],
                  consumer_secret=[CONSUMER_SECRET],
                  access_token_key=[ACCESS_TOKEN],
                  access_token_secret=[ACCESS_TOKEN_SECRET],
                  sleep_on_rate_limit=True)

print(api.)

