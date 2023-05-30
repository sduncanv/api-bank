import json


def hello(event, context):
    body = {"message": "Welcome to the app!"}

    response = {"statusCode": 200, "body": json.dumps(body)}
    return response
