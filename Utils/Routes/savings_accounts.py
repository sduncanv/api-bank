import json
from datetime import datetime

from sqlalchemy import insert, update, select

from Utils.tools import (
    http_method_validation, responses, get_a_customer, get_a_account,
    get_token_user, consult_permission, get_a_user
)
from Database.connection import run_query
from Models.users_models import SavingsAccounts
from Classes.users_classes import SavingsAccountCreate, SavingsAccountUpdate
from Utils.permissions import permissions


class SavingsAccount:

    def query_create(self, event):
        """This method creates a savings account."""

        token = event["headers"]["Authorization"][7:]
        user = get_token_user(token_user=token)

        user_with_permission = consult_permission(
            user=user, permission=permissions['savings_accounts']
        )

        if not user_with_permission:
            raise Exception(
                "The user doesn't have permissions for this module."
            )

        body = json.loads(event['body'])

        body_validation = SavingsAccountCreate(
            customer_id=body['customer_id'],
            account_number=body['account_number'],
            current_balance=body['current_balance'],
            activated_at=body['activated_at'],
            city=body['city'],
            country=body['country']
        )

        if http_method_validation(event) and body_validation:
            data_found_user = get_a_customer(id=body['customer_id'])

            if not data_found_user:
                raise Exception('The customer not exist.')

            account_found = get_a_account(
                account_number=body['account_number']
            )

            if account_found:
                raise Exception('The account already exist.')

            else:
                account_date = datetime.strptime(
                    body["activated_at"], "%Y-%m-%d"
                )
                data_found_account = get_a_account(
                    account_number=body['account_number']
                )

                if not data_found_account:
                    found_user = get_a_user(username=user)

                    if not found_user:
                        raise Exception("Username doesn't exist.")

                    query = insert(SavingsAccounts).values(
                        user_id=found_user['user_id'],
                        customer_id=body['customer_id'],
                        account_number=body['account_number'],
                        current_balance=body['current_balance'],
                        activated_at=str(account_date),
                        city=body['city'],
                        country=body['country']
                    )
                    run_query(query)

                    mess = {
                        'Message': 'Savings account created.',
                        'Data savings account': body
                    }
                    response = responses(201, mess)
                    return response

                else:
                    raise Exception('Existing account number.')

    def query_get(self, event):
        """This method gets all savings accounts."""

        token = event["headers"]["Authorization"][7:]
        user = get_token_user(token_user=token)

        user_with_permission = consult_permission(
            user=user, permission=permissions['savings_accounts']
        )

        if not user_with_permission:
            raise Exception(
                "The user doesn't have permissions for this module."
            )

        query = select(SavingsAccounts).where(
            SavingsAccounts.account_id >= 1
        )
        savings_account = run_query(query)

        data_savings_account = [row._mapping for row in savings_account]
        li = []

        for di in data_savings_account:
            info_user = {
                key: value for (key, value) in di.items() if (
                    key != 'updated_at'
                )
            }
            li.append(info_user)

        message = {'Savings account': li}
        response = responses(200, message)
        return response

    def query_update(self, event):
        """This method updates a savings account."""

        token = event["headers"]["Authorization"][7:]
        user = get_token_user(token_user=token)

        user_with_permission = consult_permission(
            user=user, permission=permissions['savings_accounts']
        )

        if not user_with_permission:
            raise Exception(
                "The user doesn't have permissions for this module"
            )

        body = json.loads(event['body'])
        http_method = http_method_validation(event)

        data_validation = SavingsAccountUpdate(
            account_id=body['account_id'],
            current_balance=body['current_balance'],
            city=body['city'],
            country=body['country'],
            active=body['active']
        )

        if http_method and data_validation:
            data_found_account = get_a_account(id_account=body['account_id'])

            if data_found_account:
                query = update(SavingsAccounts).where(
                    SavingsAccounts.account_id == body['account_id']
                ).values(
                    account_id=body['account_id'],
                    current_balance=body['current_balance'],
                    city=body['city'],
                    country=body['country'],
                    active=body['active']
                )
                run_query(query)

                mess = {'Message': 'Updated savings account'}
                response = responses(200, mess)
                return response

            else:
                raise Exception("The savings account doesn't exist")
