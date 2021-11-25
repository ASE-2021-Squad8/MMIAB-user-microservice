def get_all_users():  # noqa: E501
    """Get users list

    Get all the users # noqa: E501


    :rtype: List[User]
    """
    return 'do some magic!'


def get_banned_users():  # noqa: E501
    """Get banned users list

    Get all the banned users # noqa: E501


    :rtype: List[User]
    """
    return 'do some magic!'


def get_black_list(user_id):  # noqa: E501
    """Get the blacklist for a user

    Get the blacklist for a user # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int

    :rtype: InlineResponse2001
    """
    return 'do some magic!'


def get_recipients(user_id):  # noqa: E501
    """Get the recipients for a user

    Get all the possible recipients for a user_id # noqa: E501

    :param user_id: 
    :type user_id: int

    :rtype: List[InlineResponse2003]
    """
    return 'do some magic!'


def get_unregistered_users():  # noqa: E501
    """Get unregistered users list

    Get all the unregistered users (inactive but not banned) # noqa: E501


    :rtype: List[User]
    """
    return 'do some magic!'


def get_user(user_id):  # noqa: E501
    """Get a user by its id

    Get a user by its id # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int

    :rtype: User
    """
    # user = UserManager.retrieve_by_id(user_id)
    # if user is None:
    #     response = {'status': 'User not present'}
    #     return jsonify(response), 404

    # return jsonify(user.serialize()), 200
    return 'do some magic!'


def get_user_by_email(user_email):  # noqa: E501
    """Get user by email

    Get a user by its email # noqa: E501

    :param user_email: User unique email
    :type user_email: str

    :rtype: User
    """
    # user = UserManager.retrieve_by_email(user_email)
    # if user is None:
    #     response = {'status': 'User not present'}
    #     return jsonify(response), 404

    # return jsonify(user.serialize()), 200
    return 'do some magic!'


def get_user_details(user_id):  # noqa: E501
    """Get a user&#x27;s public details

    Get a user&#x27;s public details by its id # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int

    :rtype: UserPublic
    """
    return 'do some magic!'


def get_user_email(user_id):  # noqa: E501
    """Get email of user

    Get the email of a user by its id # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int

    :rtype: InlineResponse2002
    """
    return 'do some magic!'


def get_users_list_json():  # noqa: E501
    """Get public users list

    Get all the users public details # noqa: E501


    :rtype: List[UserPublic]
    """
    return 'do some magic!'
