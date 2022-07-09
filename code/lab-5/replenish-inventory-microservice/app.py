import boto3
import base64
import json


def lambda_handler(event, context):
    print("Lambda invoked!")
    sns_client = boto3.client('sns')    
    for record in event["Records"]:
        decoded_data = json.loads(
            base64.b64decode(record["kinesis"]["data"]).decode("utf-8")
        )
        print("Here is a message..")
        print(decoded_data)
        print(type(decoded_data))
        print(decoded_data.get("eventName", None))
        if decoded_data["eventName"] == "INSERT":
            inserted_data = decoded_data["dynamodb"]["NewImage"]
            print(f"New customer joined! Customer name is {inserted_data['region']['S']}")
            sns_client.publish(TopicArn='arn:aws:sns:us-east-2:170291251086:RideReplenishTopic',Message='More Rides Added',Subject='Replinish Ride')
        if decoded_data["eventName"] == "MODIFY":
            old_data = decoded_data["dynamodb"]["OldImage"]
            new_data = decoded_data["dynamodb"]["NewImage"]
            print(
                f"Customer updated! Old region was {old_data['region']['S']} and new name is {new_data['region']['S']}"
            )
        if decoded_data["eventName"] == "REMOVE":
            deleted_data = decoded_data["dynamodb"]["OldImage"]
            print(
                f"Customer removed! Send farewell email to: {deleted_data['region']['S']}"
            )
    return {"statusCode": 200, "body": json.dumps("Hello from Lambda!")}