import json
from datetime import date, datetime

from sqlalchemy import insert, select

from Classes.users_classes import CreateCredits
from Utils.tools import (
    http_method_validation, get_a_customer, responses, get_token_user,
    consult_permission, get_a_user
)
from Models.users_models import Credit
from Database.connection import run_query
from Utils.permissions import permissions


class Credits:

    def query_create(self, event):
        """This method creates a credit."""

        token = event["headers"]["Authorization"][7:]
        user = get_token_user(token_user=token)

        user_with_permission = consult_permission(
            user=user, permission=permissions['credits']
        )

        if not user_with_permission:
            raise Exception(
                "The user doesn't have permissions for this module"
            )

        body = json.loads(event['body'])
        body_customer_id = body['customer_id']
        body_credit_value = body['credit_value']
        payment_date = body['payment_date']

        body_validation = CreateCredits(
            customer_id=body_customer_id,
            credit_value=body_credit_value,
            fee=body['fee'],
            months_term=body['months_term'],
            payment_date=payment_date
        )

        if http_method_validation(event) and body_validation:
            customer = get_a_customer(id=body_customer_id)

            if not customer:
                raise Exception('The customer not exist.')

            else:
                if payment_date not in range(1, 32):
                    raise Exception('Select a valid day of the month.')

                day = date.today()

                found_user = get_a_user(username=user)
                if not found_user:
                    raise Exception("Username doesn't exist.")

                query = insert(Credit).values(
                    user_id=found_user['user_id'],
                    customer_id=body_customer_id,
                    credit_value=body_credit_value,
                    fee=body['fee'],
                    months_term=body['months_term'],
                    payment_date=payment_date,
                    next_payment=str(datetime.strptime(
                        f"{payment_date}-{day.month+1}-{day.year}", "%d-%m-%Y"
                    )),
                    current_balance=body_credit_value
                )
                run_query(query)

                mess = {
                    'Message': 'Created credit', 'Data credit': body
                }
                response = responses(201, mess)
                return response

    def query_get(self, event):
        """This method gets all the credits."""

        token = event["headers"]["Authorization"][7:]
        user = get_token_user(token_user=token)

        user_with_permission = consult_permission(
            user=user, permission=permissions['credits']
        )

        if not user_with_permission:
            raise Exception(
                "The user doesn't have permissions for this module"
            )

        query = select(Credit).where(Credit.credit_id >= 1)
        credit = run_query(query)
        data_credit = [row._mapping for row in credit]
        li = []

        for di in data_credit:
            info_user = {
                key: value for key, value in di.items() if (
                    key != 'created_at'
                )
            }
            li.append(info_user)

        message = {'Credits': li}
        response = responses(200, message)
        return response
