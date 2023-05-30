import json
import boto3

from Utils.tools import responses
from Classes.users_classes import LoginTokens


def query_token(event):
    """This function gets and updates a user's access token."""

    login_data = json.loads(event['body'])

    body_validation = LoginTokens(
        username=login_data['username'],
        password=login_data['password']
    )

    if body_validation:

        client_cognito = boto3.client('cognito-idp')
        respon = client_cognito.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': login_data['username'],
                'PASSWORD': login_data['password']
            },
            ClientId='329pqsbehgs5vj0oo2li4vi2l7'
        )

        mess = {'Message Lambda': respon}
        response = responses(200, mess)
        return response
