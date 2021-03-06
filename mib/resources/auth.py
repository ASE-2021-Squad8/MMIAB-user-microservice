from mib.dao.user_manager import UserManager
from flask import jsonify
from mib.resources.query import user_dict


def authenticate(auth):
    """
    Authentication resource for generic user.
    :param auth: a dict with email and password keys.
    :return: the response 200 if credentials are correct, else 401
    """
    user = UserManager.retrieve_by_email(auth['email'])
    response = {
        'authentication': 'failure',
        'user': None
    }
    response_code = 400

    if user and user.is_active and user.authenticate(auth['password']):
        response['authentication'] = 'success'
        response['user'] = user_dict(user)
        response_code = 200

    return jsonify(response), response_code
