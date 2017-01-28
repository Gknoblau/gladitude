import boto.dynamodb
from boto.dynamodb.schema import Schema

conn = boto.dynamodb.connect_to_region(
        'us-west-2',
        aws_access_key_id='AKIAIIMMXJREASSBQ6ZA',
        aws_secret_access_key='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')

table = conn.table_from_schema(
        name='tweets',
        schema=Schema.create(hash_key=('forum_name', 'S'),
                             range_key=('subject', 'S')))

