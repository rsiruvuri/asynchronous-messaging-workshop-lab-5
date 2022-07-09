import json
import boto3
from botocore.config import Config
import random
import uuid
import os
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_NAME = os.environ['TABLE_NAME']

config = Config(connect_timeout=5, read_timeout=5, retries={'max_attempts': 1})
dynamodb = boto3.client('dynamodb', config=config)

def is_invalid(request):
    # TODO validate all input fields
    # request['from']
    return False
    
def lambda_handler(event, context):
    print('EVENT: {}'.format(json.dumps(event)))

    request = json.loads(event['Records'][0]['body'])
    print('The request loaded ' + str(request))    

    print("-------------str(request['Region'])-------------------------",str(request['region']))
    print("-------------(request['Region'])-------------------------",request['region'])
    print("-------------TABLE_NAME-------------------------",TABLE_NAME)    
    
    if is_invalid(request):
        return {
            'statusCode': 400,
            'body': json.dumps({})
        }

    print('Request is valid!')
    
    id = str(uuid.uuid4())
    request['id'] = id
    
    response = dynamodb.put_item(
        TableName=TABLE_NAME,
        Item={
            'id': {'S': id},
            'from': {'S': request['from']},
            'to': {'S': request['to']},
            'duration': {'N': str(request['duration'])},
            'distance': {'N': str(request['distance'])},
            'region': {'S': request['region']},
            'customer': {'S': request['customer']},
            'fare': {'N': str(request['fare'])}
        }
    )
    
    return {
        'statusCode': 201,
        'body': json.dumps({
            "id": id
        })
    }