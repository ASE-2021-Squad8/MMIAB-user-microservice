from flask import request, jsonify

def add_points(body, user_id):  # noqa: E501
    """Change number of points for user

    Change number of points for user # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param user_id: User Unique ID
    :type user_id: int

    :rtype: None
    """
    if connexion.request.is_json:
        body = PointsUserIdBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def change_data_user(body, user_id):  # noqa: E501
    """Modify user data

    Change the account data of a user # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param user_id: User Unique ID
    :type user_id: int

    :rtype: None
    """
    if connexion.request.is_json:
        body = DataUserIdBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def change_pass_user(body, user_id):  # noqa: E501
    """Change user password

    Change the password of a user # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param user_id: User Unique ID
    :type user_id: int

    :rtype: None
    """
    if connexion.request.is_json:
        body = PasswordUserIdBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def create_user(body):  # noqa: E501
    """Add a new user

     # noqa: E501

    :param body: Create a new user inside microservice app
    :type body: dict | bytes

    :rtype: None
    """
    # if connexion.request.is_json:
    #     body = UserBody.from_dict(connexion.request.get_json())  # noqa: E501

    # post_data = request.get_json()
    # email = post_data.get('email')
    # password = post_data.get('password')

    # searched_user = UserManager.retrieve_by_email(email)
    # if searched_user is not None:
    #     return jsonify({
    #         'status': 'Already present'
    #     }), 200

    # user = User()
    # birthday = datetime.datetime.strptime(post_data.get('birthdate'),
    #                                       '%Y-%m-%d')
    # user.set_email(email)
    # user.set_password(password)
    # user.set_first_name(post_data.get('firstname'))
    # user.set_last_name(post_data.get('lastname'))
    # user.set_birthday(birthday)
    # user.set_phone(post_data.get('phone'))
    # UserManager.create_user(user)

    # response_object = {
    #     'user': user.serialize(),
    #     'status': 'success',
    #     'message': 'Successfully registered',
    # }

    # return jsonify(response_object), 201
    return 'do some magic!'


def modify_black_list(body, user_id):  # noqa: E501
    """Put/delete users in/from blacklist

    Put/delete users in/from the blacklist of user_id # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param user_id: User Unique ID
    :type user_id: int

    :rtype: InlineResponse2001
    """
    if connexion.request.is_json:
        body = BlackListUserIdBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def report(body):  # noqa: E501
    """Report a user

    Report a user by its email # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = UserReportBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def set_content_filter(body, user_id):  # noqa: E501
    """Set content filter for user

    Change the content filter of a user # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param user_id: User Unique ID
    :type user_id: int

    :rtype: None
    """
    if connexion.request.is_json:
        body = ContentFilterUserIdBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def unregister(user_id):  # noqa: E501
    """Unregister a user

    Unregister a user by its id (set is_active to false) # noqa: E501

    :param user_id: 
    :type user_id: int

    :rtype: None
    """
    # UserManager.delete_user_by_id(user_id)
    # response_object = {
    #     'status': 'success',
    #     'message': 'Successfully deleted',
    # }

    # return jsonify(response_object), 202
    return 'do some magic!'
