import json
from datetime import datetime

from sqlalchemy import insert, update, select

from Utils.tools import (
    http_method_validation, responses, get_a_customer, get_token_user,
    consult_permission, get_a_user
)
from Database.connection import run_query
from Models.users_models import Transactions, SavingsAccounts
from Classes.users_classes import TransactionCreate
from Utils.permissions import permissions


class Transaction:

    def query_create(self, event):
        """This method creates a transaction."""

        token = event["headers"]["Authorization"][7:]
        user = get_token_user(token_user=token)

        user_with_permission = consult_permission(
            user=user, permission=permissions['transactions']
        )

        if not user_with_permission:
            raise Exception(
                "The user doesn't have permissions for this module"
            )

        body = json.loads(event['body'])

        body_validation = TransactionCreate(
            customer_id=body['customer_id'],
            account_number=body['account_number'],
            transaction_date=body['transaction_date'],
            trade_name=body['trade_name'],
            transaction_value=body['transaction_value'],
            trade_status=body['trade_status']
        )

        if http_method_validation(event) and body_validation:
            query = select(SavingsAccounts).where(
                SavingsAccounts.customer_id == body['customer_id'],
                SavingsAccounts.account_number == body['account_number'],
                SavingsAccounts.active == 1
            )
            found_account = run_query(query)
            data_found_account = [row._mapping for row in found_account]

            if not data_found_account:
                raise Exception('The account not exist.')

            cust_found = get_a_customer(id=body['customer_id'])

            if not cust_found:
                raise Exception('The customer not exist.')

            else:
                transaction_value = int(body['transaction_value'])
                current_balance = int(data_found_account[0]['current_balance'])
                ending_balance = current_balance - transaction_value
                transaction_date = datetime.strptime(
                    body["transaction_date"], "%Y-%m-%d"
                )

                found_user = get_a_user(username=user)
                if not found_user:
                    raise Exception('Username does not exist.')

                query = insert(Transactions).values(
                    user_id=found_user['user_id'],
                    customer_id=body['customer_id'],
                    account_number=body['account_number'],
                    transaction_date=str(transaction_date),
                    trade_name=body['trade_name'],
                    transaction_value=body['transaction_value'],
                    current_balance=current_balance,
                    ending_balance=ending_balance,
                    trade_status=body['trade_status']
                )
                run_query(query)

                if body['trade_status'] == 1:
                    if current_balance == 0:
                        raise Exception('The account has no money.')

                    if int(transaction_value) > current_balance:
                        raise Exception(
                            'The transaction exceeds current balance.'
                        )

                    query2 = update(SavingsAccounts).where(
                        SavingsAccounts.account_number == body['account_number'],
                        SavingsAccounts.active == 1
                    ).values(
                        current_balance=current_balance - transaction_value
                    )
                    run_query(query2)

                mess = {
                    'Message': 'Transaction created', 'Data transaction': body
                }
                response = responses(201, mess)
                return response

    def get_transaction(self, event):
        """This method gets all the transactions."""

        token = event["headers"]["Authorization"][7:]
        user = get_token_user(token_user=token)

        user_with_permission = consult_permission(
            user=user, permission=permissions['transactions']
        )

        if not user_with_permission:
            raise Exception(
                "The user doesn't have permissions for this module"
            )

        query = select(Transactions).where(Transactions.transactions_id >= 1)
        transactions = run_query(query)

        data_transactions = [row._mapping for row in transactions]
        li = []

        for di in data_transactions:
            info_user = {
                key: value for (key, value) in di.items() if (
                    key != 'updated_at'
                )
            }
            li.append(info_user)

        message = {'Transactions': li}
        response = responses(200, message)
        return response
