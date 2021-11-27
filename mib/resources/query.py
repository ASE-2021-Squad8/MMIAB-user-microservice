from mib.dao.user_manager import UserManager
from mib.resources.users import jsonify_response, error404user


def get_all_users():  # noqa: E501
    """Get users list # noqa: E501

    :rtype: List[User]
    """
    all_users = UserManager.get_all_users()
    return jsonify_response(200, all_users)


def get_banned_users():  # noqa: E501
    """Get all the banned users # noqa: E501

    :rtype: List[User]
    """
    banned_users = UserManager.get_banned_users()
    return jsonify_response(200, banned_users)


def get_black_list(user_id):  # noqa: E501
    """Get the blacklist for a user # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int

    :rtype: InlineResponse2001
    """
    blacklist = UserManager.get_blacklisted(user_id)
    return jsonify_response(200, blacklist)


def get_recipients(user_id):  # noqa: E501
    """Get all the possible recipients for a user_id # noqa: E501

    :param user_id:
    :type user_id: int

    :rtype: List[InlineResponse2003]
    """
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        return error404user()

    recipients = UserManager.get_recipients(user_id)
    return jsonify_response(200, recipients)


def get_unregistered_users():  # noqa: E501
    """Get all the unregistered users (inactive but not banned) # noqa: E501

    :rtype: List[User]
    """
    unregistered_users = UserManager.get_unregistered_users()
    return jsonify_response(200, unregistered_users)


def get_user(user_id):  # noqa: E501
    """Get a user by its id # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int

    :rtype: User
    """
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        return error404user()

    return jsonify_response(200, user)


def get_user_by_email(user_email):  # noqa: E501
    """Get a user by its email # noqa: E501

    :param user_email: User unique email
    :type user_email: str

    :rtype: User
    """
    user = UserManager.retrieve_by_email(user_email)
    if user is None:
        return error404user()

    return jsonify_response(200, user)


def get_user_public(user_id):  # noqa: E501
    """Get a user's public details by its id # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int

    :rtype: UserPublic
    """
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        return error404user()

    public_user = {
        "firstname": user.firstname,
        "lastname": user.lastname,
        "email": user.email,
    }

    return jsonify_response(200, public_user)


def get_user_email(user_id):  # noqa: E501
    """Get the email of a user by its id # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int

    :rtype: InlineResponse2002
    """
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        return error404user()

    return jsonify_response(200, user.email)


def get_all_users_public():  # noqa: E501
    """Get public users list # noqa: E501

    :rtype: List[UserPublic]
    """
    public_users = UserManager.get_all_users_public()
    return jsonify_response(200, public_users)
