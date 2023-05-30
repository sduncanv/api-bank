import json
import jwt

from sqlalchemy import select, or_, and_
from Models.users_models import (
    User, Customer, SavingsAccounts, Transactions, Credit, Permission
)
from Database.connection import run_query


def http_method_validation(event):
    """"
    This function validates the http method of the event.
    Returns True if the event is successful or raises an error if not.
    """
    method = event['requestContext']['httpMethod']

    if method == 'POST' or method == 'PUT':
        if not event['body']:
            raise Exception(
                f'For the {method} method, the body must have content'
            )

        return True

    elif method == 'GET' or method == 'DELETE':
        if event['queryStringParameters'] is None:

            raise Exception(
                f'For the {method} method, parameters are expected in the path'
            )

        return True


def get_a_user(username=None, document=None, email=None, id=None):
    """
    This function gets a user in the database.
    Returns the user found or False if the user doesn't exist.
    """
    query = select(User).where(
        or_(
            User.username == username,
            User.document == document,
            User.email == email,
            User.user_id == id
        )
    )
    found_user = run_query(query)
    data_found_user = [row._mapping for row in found_user]

    if data_found_user:
        return data_found_user[0]

    else:
        return False


def get_a_customer(email=None, id=None, document=None):
    """
    This function gets a customer in the database.
    Returns the customer found or False if the customer doesn't exist.
    """
    query = select(Customer).where(
        and_(
            Customer.active == 1,
            or_(
                Customer.email == email,
                Customer.customer_id == id,
                Customer.document == document
            )
        )
    )
    found_user = run_query(query)
    data_found_user = [row._mapping for row in found_user]

    if data_found_user:
        return data_found_user[0]

    else:
        return False


def get_a_account(account_number=None, id_cus=None, id_account=None):
    """
    This function gets a savings account in the database.
    Returns the savings account found or False if doesn't exist.
    """
    query = select(SavingsAccounts).where(
        and_(
            SavingsAccounts.active == 1,
            or_(
                SavingsAccounts.customer_id == id_cus,
                SavingsAccounts.account_number == account_number,
                SavingsAccounts.account_id == id_account
            )
        )
    )
    found_user = run_query(query)
    data_found_user = [row._mapping for row in found_user]

    if data_found_user:
        return data_found_user[0]

    else:
        return False


def get_a_transaction(id=None):
    """
    This function gets a transaction in the database.
    Returns the transaction found or False if the transaction doesn't exist.
    """
    query = select(Transactions).where(Transactions.transactions_id == id)

    found_user = run_query(query)
    data_found_user = [row._mapping for row in found_user]

    if data_found_user:
        return data_found_user[0]

    else:
        return False


def get_a_credit(id=None):
    """
    This function gets a credit in the database.
    Returns the credit found or False if the credit doesn't exist.
    """
    query = select(Credit).where(
        Credit.credit_id == id,
        Credit.status_credit == 1
    )
    found_credit = run_query(query)

    data_found_credit = [row._mapping for row in found_credit]

    if data_found_credit:
        return data_found_credit[0]

    else:
        return False


def responses(status_code, message) -> dict:
    """
    This function creates the http response with a status code and a message.
    """
    respon = {
        'statusCode': status_code,
        'body': json.dumps(message),
    }
    return respon


def get_token_user(token_user):
    """
    This function decodes the event token.
    Returns the username found in the token.
    """
    response = jwt.decode(
        token_user,
        algorithms=["RS256"],
        options={"verify_signature": False}
    )
    user = response['custom:username']
    return user


def consult_permission(user, permission):
    """
    This function gets the permissions of a user in the database.
    Parameters:
        - user: user who consumes the module
        - permission: module
    Returns True if the user has the permission or False if the user doesn't.
    """
    query = select(Permission).where(
        Permission.user == user,
        Permission.permission == permission
    )
    found_permission = run_query(query)
    data_found = [row._mapping for row in found_permission]

    if data_found:
        return True

    else:
        return False
