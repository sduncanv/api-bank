from sqlalchemy import select

from Utils.tools import http_method_validation, responses
from Models.users_models import Permission
from Classes.users_classes import VerifyUsername
from Database.connection import run_query


permissions = {
    'users': 0,
    'customers': 1,
    'savings_accounts': 2,
    'transactions': 3,
    'credits': 4,
    "fee": 5
}


def query_get_permissions(event):
    """
    This role assigns permissions to a user.
    """
    data = event['queryStringParameters']
    http_method = http_method_validation(event)
    data_validation = VerifyUsername(username=data['user'])
    # data_validation = type(data['user']) == str

    if http_method and data_validation:
        query = select(Permission).where(Permission.user == data['user'])
        permission = run_query(query)
        data_permission = [row._mapping for row in permission]

        li = []
        for di in data_permission:
            info_permission = {key: value for key, value in di.items()}
            li.append(info_permission)

        li_user = []
        for i in li:
            a = i['permission']
            if a not in li_user:
                li_user.append(a)

        if li:
            message = {f"Permissions {str(data['user'])}": li_user}
            response = responses(200, message)
            return response

        else:
            raise Exception("The user doesn't have permissions.")
