from Utils.exceptions import try_except
from Utils.Routes.customers import Customers
from Utils.Routes.savings_accounts import SavingsAccount
from Utils.Routes.transactions import Transaction
from Utils.Routes.users import (
    query_create, query_auth_user, query_get, query_assign, query_update
)
from Utils.Routes.tokens import query_token
from Utils.Routes.credits import Credits
from Utils.Routes.fee import Installments
# from Utils.Pools.users_pools import pool_users
from Utils.permissions import query_get_permissions


customer = Customers()
savings_account = SavingsAccount()
transaction = Transaction()
credits = Credits()
installments = Installments()


@try_except
def create_user(event, context):
    response = query_create(event)
    return response


# @try_except
# def presignup(event, context):
#     response = pool_users(event)
#     return response


@try_except
def get_users(event, context):
    response = query_get(event)
    return response


@try_except
def update_user(event, context):
    response = query_update(event)
    return response


@try_except
def auth_user(event, context):
    response = query_auth_user(event)
    return response


@try_except
def login(event, context):
    response = query_token(event)
    return response


@try_except
def assign_permissions(event, context):
    response = query_assign(event)
    return response


@try_except
def get_permissions(event, context):
    response = query_get_permissions(event)
    return response


@try_except
def create_customer(event, context):
    response = customer.query_create(event)
    return response


@try_except
def update_customer(event, context):
    response = customer.query_update(event)
    return response


@try_except
def get_customers(event, context):
    response = customer.query_get(event)
    return response


@try_except
def delete_customer(event, context):
    response = customer.query_delete(event)
    return response


@try_except
def create_savings_account(event, context):
    response = savings_account.query_create(event)
    return response


@try_except
def get_savings_account(event, context):
    response = savings_account.query_get(event)
    return response


@try_except
def update_savings_account(event, context):
    response = savings_account.query_update(event)
    return response


# @try_except
# def delete_savings_account(event, context):
#     response = savings_account.query_delete(event)
#     return response


@try_except
def create_transaction(event, context):
    response = transaction.query_create(event)
    return response


@try_except
def get_transaction(event, context):
    response = transaction.get_transaction(event)
    return response


@try_except
def create_credits(event, context):
    response = credits.query_create(event)
    return response


@try_except
def get_credit(event, context):
    response = credits.query_get(event)
    return response


@try_except
def create_installments(event, context):
    response = installments.query_create(event)
    return response


@try_except
def get_installments(event, context):
    response = installments.query_get(event)
    return response
