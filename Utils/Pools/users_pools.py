# import json
# import boto3


# def pool_users(event):
#     body = json.loads(event['body'])
#     phoneNumber = str(body['phone_number'])

#     client_cognito = boto3.client('cognito-idp')

#     client_cognito.sign_up(
#         ClientId='47vje27fgjujp7gh2e7d0afmt4',
#         Username=body['username'],
#         Password=body['password'],
#         UserAttributes=[
#             {'Name': 'name', 'Value': body['name']},
#             {'Name': 'custom:document', 'Value': body['document']},
#             {'Name': 'phone_number', 'Value': phoneNumber},
#             {'Name': 'email', 'Value': body['email']},
#             {'Name': 'custom:age', 'Value': body['age']},
#             {'Name': 'preferred_username', 'Value': body['username']},
#             {'Name': 'custom:password', 'Value': body['password']}
#         ]
#     )

#     response = 'Created in cognito'
#     return response
