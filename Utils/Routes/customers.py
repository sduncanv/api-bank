import json
import boto3
import base64

from sqlalchemy import insert, select, update, and_
from pymysql import IntegrityError

from Utils.tools import (
    http_method_validation, responses, get_a_customer, get_token_user,
    consult_permission, get_a_user
)
from Database.connection import run_query
from Models.users_models import Customer
from Classes.users_classes import RegisterCustomer, VerifyId
from Utils.permissions import permissions


class Customers:

    def query_create(self, event):
        """This method creates a customer."""

        token = event["headers"]["Authorization"][7:]
        user = get_token_user(token_user=token)

        user_with_permission = consult_permission(
            user=user, permission=permissions['customers']
        )

        if not user_with_permission:
            raise Exception(
                "The user doesn't have permissions for this module"
            )

        body = json.loads(event['body'])
        img = base64.b64decode(body['selfie'])

        body_validation = RegisterCustomer(
            name=body['name'],
            document=body['document'],
            phone_number=body['phone_number'],
            email=body['email'],
            age=body['age'],
            address=body['address'],
            city=body['city'],
            profession=body['profession'],
            selfie=body['selfie']
        )

        if http_method_validation(event) and body_validation:
            data_found_user = get_a_customer(
                email=body['email'], document=body['document']
            )

            found_user = get_a_user(username=user)

            if not found_user:
                raise Exception("Username doesn't exist.")

            if not data_found_user:

                query = insert(Customer).values(
                    user_id=found_user['user_id'],
                    name=body['name'].title(),
                    document=body['document'],
                    phone_number=body['phone_number'],
                    email=body['email'],
                    age=body['age'],
                    address=body['address'],
                    city=body['city'],
                    profession=body['profession'],
                    selfie=img
                )

                client_cognito = boto3.resource('s3')
                client_cognito.Object(
                    "bucket1-apibank",
                    f"photo_customer_{body['document']}.jpg"
                ).put(Body=img)

                run_query(query)

                mess = {'Message': 'Signup successful', 'Data customer': body}
                response = responses(200, mess)
                return response

            else:
                raise Exception('The email or document already exist.')

    def query_update(self, event):
        """This method updates a customer."""

        token = event["headers"]["Authorization"][7:]
        user = get_token_user(token_user=token)

        user_with_permission = consult_permission(
            user=user, permission=permissions['customers']
        )

        if not user_with_permission:
            raise Exception(
                "The user doesn't have permissions for this module"
            )

        body = json.loads(event['body'])
        img = base64.b64decode(body['selfie'])

        data_validation = RegisterCustomer(
            name=body['name'],
            document=body['document'],
            phone_number=body['phone_number'],
            email=body['email'],
            age=body['age'],
            address=body['address'],
            city=body['city'],
            profession=body['profession'],
            selfie=body['selfie']
        )

        if http_method_validation(event) and data_validation:
            custo = get_a_customer(id=body['customer_id'])

            if not custo:
                raise Exception("Customer doesn't exist.")

            query = select(Customer).where(
                and_(
                    Customer.email == body['email'],
                    Customer.active == 1,
                    Customer.customer_id != body['customer_id']
                )
            )
            emails = run_query(query)
            email_not_available = [row._mapping for row in emails]

            if email_not_available:
                raise IntegrityError('The email is not available.')

            query2 = update(Customer).where(
                Customer.customer_id == body['customer_id']
            ).values(
                name=body['name'],
                document=body['document'],
                phone_number=body['phone_number'],
                email=body['email'],
                age=body['age'],
                address=body['address'],
                city=body['city'],
                profession=body['profession'],
                selfie=img
            )
            client_cognito = boto3.resource('s3')
            client_cognito.Object(
                "bucket1-apibank",
                f"photo_customer_{custo['document']}.jpg"
            ).put(Body=img)

            changes = run_query(query2)

            if type(changes) is dict:
                raise IntegrityError('Error en los datos.')

            else:
                mess = {
                    'Message': 'Updated customer', 'Updated data': body
                }
                response = responses(201, mess)
                return response

    def query_delete(self, event):
        """This method deletes a customer."""

        token = event["headers"]["Authorization"][7:]
        user = get_token_user(token_user=token)

        user_with_permission = consult_permission(
            user=user, permission=permissions['customers']
        )

        if not user_with_permission:
            raise Exception(
                "The user doesn't have permissions for this module"
            )

        data = event['queryStringParameters']
        http_method = http_method_validation(event)

        if data is not None:
            data_validation = VerifyId(id=data['customer_id'])
            # data_validation = DeleteCustomer(customer_id=data['customer_id'])

        if http_method and data_validation:
            data_found_customer = get_a_customer(id=data['customer_id'])

            if data_found_customer:
                query = update(Customer).where(
                    Customer.customer_id == data['customer_id']
                ).values(active=0)
                run_query(query)

                mess = {'Message': 'Customer deleted.'}
                response = responses(200, mess)
                return response

            else:
                raise Exception("The customer doesn't exist.")

    def query_get(self, event):
        """This method gets all customers."""

        token = event["headers"]["Authorization"][7:]
        user = get_token_user(token_user=token)

        user_with_permission = consult_permission(
            user=user, permission=permissions['customers']
        )

        if not user_with_permission:
            raise Exception(
                "The user doesn't have permissions for this module."
            )

        query = select(Customer).where(Customer.customer_id >= 1)
        customers = run_query(query)

        data_customers = [row._mapping for row in customers]
        li = []

        for di in data_customers:
            info_customer = {
                key: value for (key, value) in di.items() if (
                    key != 'created_at' and
                    key != 'selfie'
                )
            }
            li.append(info_customer)

        message = {'Customers': li}
        response = responses(200, message)
        return response
