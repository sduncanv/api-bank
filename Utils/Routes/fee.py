import json
from datetime import datetime, date

from sqlalchemy import update, insert, select

from Classes.users_classes import CreateInstallments, VerifyId
from Models.users_models import Credit, Installment
from Utils.tools import (
    http_method_validation, responses, get_a_credit, get_token_user,
    consult_permission, get_a_user
)
from Database.connection import run_query
from Utils.permissions import permissions


class Installments:

    def query_create(self, event):
        """This method creates a fee."""

        token = event["headers"]["Authorization"][7:]
        user = get_token_user(token_user=token)

        user_with_permission = consult_permission(
            user=user, permission=permissions['fee']
        )

        if not user_with_permission:
            raise Exception(
                "The user doesn't have permissions for this module"
            )

        body = json.loads(event['body'])
        change = False

        body_validation = CreateInstallments(
            credit_id=body['credit_id'],
            installments_value=body['installments_value'],
            installments_date=body["installments_date"]
        )

        if http_method_validation(event) and body_validation:
            credit = get_a_credit(id=body['credit_id'])

            if not credit:
                raise Exception('The credit not exist.')

            current_balance = int(credit['current_balance'])
            credit_status = 1

            if current_balance <= 0:
                mess = {'Message': 'You currently owe no money.'}
                response = responses(200, mess)
                return response

            installments_value = int(body['installments_value'])

            if installments_value > current_balance:
                change = True
                changes_value = installments_value - current_balance
                installments_value = installments_value - changes_value
                credit_status = 0

            if current_balance - installments_value == 0:
                credit_status = 0

            day = date.today()
            payment_date = credit['payment_date']
            ins_date = datetime.strptime(body["installments_date"], "%Y-%m-%d")

            query2 = update(Credit).where(
                Credit.credit_id == body['credit_id']
            ).values(
                current_balance=current_balance - installments_value,
                dues_paid=credit['dues_paid'] + 1,
                next_payment=datetime.strptime(
                    f"{payment_date}-{day.month+1}-{day.year}", "%d-%m-%Y"
                ),
                last_payment=str(ins_date),
                status_credit=credit_status
            )

            found_user = get_a_user(username=user)
            if not found_user:
                raise Exception("Username doesn't exist.")

            query3 = insert(Installment).values(
                user_id=found_user['user_id'],
                credit_id=body['credit_id'],
                installment_value=body['installments_value'],
                installment_date=str(ins_date)
            )
            run_query(query2)
            run_query(query3)

            if change:
                mess = {
                    'Message': f"Debt paid, you'll have {changes_value} back",
                    'Data payment': body
                }
                response = responses(201, mess)
                return response

            else:
                mess = {'Message': 'Registered payment', 'Data payment': body}
                response = responses(201, mess)
                return response

    def query_get(self, event):
        """This method gets all the fees of a credit."""

        token = event["headers"]["Authorization"][7:]
        user = get_token_user(token_user=token)

        user_with_permission = consult_permission(
            user=user, permission=permissions['fee']
        )

        if not user_with_permission:
            raise Exception(
                "The user doesn't have permissions for this module"
            )

        data = event['queryStringParameters']
        http_method = http_method_validation(event)
        data_validation = VerifyId(id=data['credit_id'])
        # data_validation = type(int(data['credit_id'])) == int

        if http_method and data_validation:
            query = select(Installment).where(
                Installment.credit_id == data['credit_id']
            )
            installments = run_query(query)
            data_installments = [row._mapping for row in installments]
            li = []

            for di in data_installments:
                info_user = {key: value for key, value in di.items()}
                li.append(info_user)

            if li:
                message = {'Credits fees': li}
                response = responses(200, message)
                return response

            else:
                raise Exception("The credit doesn't no fees.")
