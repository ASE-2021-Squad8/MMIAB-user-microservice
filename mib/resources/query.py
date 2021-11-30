from flask import jsonify
from mib.dao.user_manager import UserManager
from mib.resources.users import jsonify_error_response, error404user


def get_all_users():  # noqa: E501
    """Get users list # noqa: E501

    :rtype: List[User]
    """
    all_users = UserManager.get_all_users()
    return jsonify(all_users), 200


def get_banned_users():  # noqa: E501
    """Get all the banned users # noqa: E501

    :rtype: List[User]
    """
    banned_users = UserManager.get_banned_users()
    return jsonify(banned_users), 200


def get_black_list(user_id):  # noqa: E501
    """Get the blacklist for a user # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int

    :rtype: List[id, email] candidates and blacklisted
    """
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        return error404user()

    candidates = UserManager.get_blacklist_candidates(user_id)
    blacklisted = UserManager.get_blacklisted(user_id)

    return jsonify({"candidates": candidates, "blacklisted": blacklisted}), 200


def get_recipients(user_id):  # noqa: E501
    """Get all the possible recipients for a user_id # noqa: E501

    :param user_id:
    :type user_id: int

    :rtype: List[id, email]
    """
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        return error404user()

    recipients = UserManager.get_recipients(user_id)
    return jsonify(recipients), 200


def get_unregistered_users():  # noqa: E501
    """Get all the unregistered users (inactive but not banned) # noqa: E501

    :rtype: List[User]
    """
    unregistered_users = UserManager.get_unregistered_users()
    return jsonify(unregistered_users), 200


def get_user(user_id):  # noqa: E501
    """Get a user by its id # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int

    :rtype: User
    """
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        return error404user()

    return jsonify(user_dict(user)), 200


def get_user_by_email(user_email):  # noqa: E501
    """Get a user by its email # noqa: E501

    :param user_email: User unique email
    :type user_email: str

    :rtype: User
    """
    user = UserManager.retrieve_by_email(user_email)
    if user is None:
        return jsonify_error_response(404, "User_email not found")

    return jsonify(user_dict(user)), 200


def get_user_public(user_id):  # noqa: E501
    """Get a user's public details by its id # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int

    :rtype: UserPublic
    """
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        return error404user()

    return jsonify(user_public_dict(user)), 200


def get_user_email(user_id):  # noqa: E501
    """Get the email of a user by its id # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int

    :rtype: string
    """
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        return error404user()

    return jsonify(email=user.email), 200


def get_all_users_public():  # noqa: E501
    """Get public users list # noqa: E501

    :rtype: List[UserPublic]
    """
    public_users = UserManager.get_all_users_public()
    return jsonify(public_users), 200


def user_public_dict(user):
    d = {
        "firstname": user.firstname,
        "lastname": user.lastname,
        "email": user.email,
    }
    return d


def user_dict(user):
    d = {
        "id": user.id,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "email": user.email,
        "dateofbirth": user.dateofbirth,
        "password": user.password,
        "reports": user.reports,
        "is_active": user.is_active,
        "points": user.points,
        "content_filter": user.content_filter,
    }
    return d