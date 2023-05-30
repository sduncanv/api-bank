import json
import boto3

from sqlalchemy import insert, select, and_, update
from werkzeug.security import generate_password_hash, check_password_hash
from pymysql import IntegrityError

from Utils.tools import (
    http_method_validation, get_a_user, responses, get_token_user,
    consult_permission
)
from Database.connection import run_query
from Models.users_models import User, Permission
from Classes.users_classes import RegisterUser, AssignPermissions, UpdateUser
from Utils.permissions import permissions


def query_create(event):
    """This function creates a user in the database and in Amazon Cognito."""

    body = json.loads(event['body'])

    body_validation = RegisterUser(
        name=body['name'],
        document=body['document'],
        phone_number=body['phone_number'],
        email=body['email'],
        age=body['age'],
        username=body['username'],
        password=body['password'],
    )

    if http_method_validation(event) and body_validation:
        data_found_user = get_a_user(
            username=body['username'],
            email=body['email'],
            document=body['document']
        )

        if not data_found_user:
            query = insert(User).values(
                name=body['name'].title(),
                document=body['document'],
                phone_number=body['phone_number'],
                email=body['email'].lower(),
                age=body['age'],
                username=body['username'].lower(),
                password=generate_password_hash(body['password'])
            )

            client_cognito = boto3.client('cognito-idp')
            phoneNumber = str(body['phone_number'])

            client_cognito.sign_up(
                ClientId='329pqsbehgs5vj0oo2li4vi2l7',
                Username=body['username'],
                Password=body['password'],
                UserAttributes=[
                    {'Name': 'name', 'Value': body['name']},
                    {'Name': 'custom:document', 'Value': body['document']},
                    {'Name': 'phone_number', 'Value': phoneNumber},
                    {'Name': 'email', 'Value': body['email']},
                    {'Name': 'custom:age', 'Value': body['age']},
                    {'Name': 'custom:username', 'Value': body['username']},
                    {'Name': 'custom:password', 'Value': body['password']}
                ]
            )
            run_query(query)

            mess = {'Message': 'Signup successful', 'Data user': body}
            response = responses(201, mess)
            return response

        else:
            raise Exception('The username, document or email already exist.')


def query_auth_user(event):
    """This function authenticates a user in Cognito."""

    validation = http_method_validation(event)

    if validation:
        login_data = json.loads(event['body'])
        found_user = get_a_user(username=login_data['username'])

        if found_user:
            validated_password = check_password_hash(
                found_user['password'], login_data['password']
            )

            if validated_password:
                client_cognito = boto3.client('cognito-idp')
                client_cognito.admin_set_user_password(
                    UserPoolId='us-east-1_lmHYBqxo7',
                    Username=login_data['username'],
                    Password=login_data['password'],
                    Permanent=True
                )

                mess = {'Message': 'Authenticated user'}
                response = responses(200, mess)
                return response

            else:
                raise Exception('Incorrect password')

        else:
            raise Exception('User not found')


def query_get(event):
    """This function gets all users."""

    token = event["headers"]["Authorization"][7:]
    user = get_token_user(token_user=token)

    user_with_permission = consult_permission(
        user=user, permission=permissions['users']
    )

    if not user_with_permission:
        raise Exception(
            "The user doesn't have permissions for this module."
        )

    query = select(User).where(User.user_id >= 1)
    transactions = run_query(query)

    data_transactions = [row._mapping for row in transactions]
    li = []

    for di in data_transactions:
        info_user = {
            key: value for (key, value) in di.items() if (key != 'created_at')
        }
        li.append(info_user)

    message = {'Users': li}
    response = responses(200, message)
    return response


def query_update(event):
    """This function updates a user."""

    token = event["headers"]["Authorization"][7:]
    user = get_token_user(token_user=token)

    user_with_permission = consult_permission(
        user=user, permission=permissions['users']
    )

    if not user_with_permission:
        raise Exception(
            "The user doesn't have permissions for this module"
        )

    body = json.loads(event['body'])

    body_validation = UpdateUser(
        user_id=body['user_id'],
        name=body['name'],
        phone_number=body['phone_number'],
        email=body['email'],
        age=body['age']
    )

    if http_method_validation(event) and body_validation:
        found_user = select(User).where(
            User.user_id == body['user_id']
        )
        usr = run_query(found_user)
        email_not_available = [row._mapping for row in usr]

        if not email_not_available:
            raise Exception('User does not exist.')

        query = select(User).where(
            and_(
                User.email == body['email'],
                User.user_id != body['user_id']
            )
        )
        emails = run_query(query)
        email_not_available = [row._mapping for row in emails]

        if email_not_available:
            raise IntegrityError('The email is not available.')

        query2 = update(User).where(User.user_id == body['user_id']).values(
            name=body['name'],
            phone_number=body['phone_number'],
            email=body['email'],
            age=body['age']
        )

        client_cognito = boto3.client('cognito-idp')
        phoneNumber = str(body['phone_number'])

        client_cognito.admin_update_user_attributes(
            UserPoolId='us-east-1_lmHYBqxo7',
            Username=user,
            UserAttributes=[
                {'Name': 'name', 'Value': body['name']},
                {'Name': 'phone_number', 'Value': phoneNumber},
                {'Name': 'email', 'Value': body['email']},
                {'Name': 'custom:age', 'Value': body['age']}
            ]
        )

        changes = run_query(query2)

        if type(changes) is dict:
            raise IntegrityError('Error en los datos.')

        else:
            mess = {
                'Message': 'Updated user', 'Updated data': body
            }
            response = responses(201, mess)
            return response


def query_assign(event):
    """This function assigns permissions to a user."""

    body = json.loads(event['body'])

    body_validation = AssignPermissions(
        user=body['user'],
        permission=body['permission']
    )

    if http_method_validation(event) and body_validation:
        data_found_user = get_a_user(username=body['user'])

        if data_found_user:
            permissions = body['permission']

            for permission in permissions:
                query = insert(Permission).values(
                    user=body['user'],
                    permission=permission
                )
                run_query(query)

            mess = {
                "Message": "Assigned permissions.",
                "Assigned permissions": body['permission']
            }
            response = responses(201, mess)
            return response

        else:
            raise Exception('The user not exist.')
