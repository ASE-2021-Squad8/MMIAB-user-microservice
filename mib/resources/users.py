import datetime
from flask import request, jsonify
from mib.dao.user_manager import UserManager
from mib.models.user import User


def error404user():
    response = {"message": "User_id not found"}
    return jsonify(response), 404


def jsonify_response(status_code, message):
    response = {"message": message}
    return jsonify(response), status_code


def add_points(user_id):  # noqa: E501
    """Change number of points for user # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int

    :rtype: None
    """
    body = request.get_json()
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        return error404user()

    UserManager.add_points(user, int(body.get("points")))
    return jsonify_response(200, "Points changed")


def change_data_user(user_id):  # noqa: E501
    """Change the account data of a user # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int

    :rtype: None
    """
    body = request.get_json()

    # check if inputs are valid
    check_mail_db = UserManager.retrieve_by_email(body.get("textemail"))
    if check_mail_db is not None and check_mail_db.id != user_id:
        return jsonify_response(409, "The email already exists in the database")

    # update the user data
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        return error404user()

    user.set_firstname(body.get("textfirstname"))
    user.set_lastname(body.get("textlastname"))
    user.set_email(body.get("textemail"))
    date_as_datetime = datetime.datetime.strptime(body.get("textbirth"), "%Y-%m-%d")
    user.set_dateofbirth(date_as_datetime)
    UserManager.commit()

    return jsonify_response(200, "User data modified")


def change_pass_user(user_id):  # noqa: E501
    """Change user password # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int

    :rtype: None
    """
    body = request.get_json()
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        return error404user()

    current_password = body.get("currentpassword")
    new_pass = body.get("newpassword")
    confirmpass = body.get("confirmpassword")
    # check that current and confirmation password are correct
    if user.authenticate(current_password):
        if new_pass == confirmpass:
            user.set_password(new_pass)
        else:
            return jsonify_response(
                422, "New password and confirmation password does not match"
            )
    else:
        return jsonify_response(401, "Wrong current password")

    UserManager.commit()

    return jsonify_response(200, "User password modified")


def create_user():  # noqa: E501
    """Add a new user # noqa: E501

    :rtype: json
    """
    body = request.get_json()
    email = body.get("email")
    password = body.get("password")

    searched_user = UserManager.retrieve_by_email(email)
    if searched_user is not None:
        return jsonify_response(200, "Already present")

    user = User()
    dateofbirth = datetime.datetime.strptime(body.get("dateofbirth"), "%Y-%m-%d")
    user.set_email(email)
    user.set_password(password)
    user.set_firstname(body.get("firstname"))
    user.set_lastname(body.get("lastname"))
    user.set_dateofbirth(dateofbirth)
    UserManager.create_user(user)

    # response = {
    #     "user": user.serialize(),
    #     "status": "success",
    #     "message": "Successfully registered",
    # }
    # return jsonify(response), 201
    return jsonify_response(201, "Created")


def modify_black_list(user_id):  # noqa: E501
    """Put/delete users in/from blacklist of user_id # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int

    :rtype: InlineResponse2001
    """
    body = request.get_json()
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        return error404user()

    # remove or add users to the blacklist
    op = body.get("op")
    members_id = body.get("users")

    if op == "delete":
        UserManager.delete_from_blacklist(user_id, members_id)
    elif op == "add":
        UserManager.add_to_blacklist(user_id, members_id)

    candidates = UserManager.get_blacklist_candidates(user_id)
    blacklisted = UserManager.get_blacklisted(user_id)

    return jsonify_response(200, {"candidates": candidates, "blacklisted": blacklisted})


def report():  # noqa: E501
    """Report a user

    Report a user by its email # noqa: E501

    :rtype: None
    """
    # get the mail of the user to be reported and report it
    body = request.get_json()
    mail = body.get("useremail")
    user = UserManager.retrieve_by_email(mail)
    if user is None:
        return error404user()

    UserManager.report(user)

    return jsonify_response(200, "User reported")


def set_content_filter(user_id):  # noqa: E501
    """Set content filter for user # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int

    :rtype: None
    """
    body = request.get_json()
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        return error404user()

    value = body.get("filter")
    value = int(value) == 1
    UserManager.set_content_filter(user, value)

    return jsonify_response(200, "Content filter set")


def unregister(user_id):  # noqa: E501
    """Unregister a user by its id (set is_active to false) # noqa: E501

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
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        return error404user()

    UserManager.unregister(user)
    return jsonify_response(200, "User unregistered")
