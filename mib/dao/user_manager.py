from mib.dao.manager import Manager
from mib.models.user import User, BlackList


class UserManager(Manager):
    @staticmethod
    def commit():
        Manager.commit()

    @staticmethod
    def create_user(user: User):
        Manager.create(user=user)

    @staticmethod
    def retrieve_by_id(id_):
        Manager.check_none(id=id_)
        return User.query.get(id_)

    @staticmethod
    def retrieve_by_email(email):
        Manager.check_none(email=email)
        return User.query.filter(User.email == email).first()

    @staticmethod
    def add_points(user: User, points_: int):
        Manager.check_none(user=user, points_=points_)
        setattr(user, "points", user.points + points_)
        Manager.commit()

    @staticmethod
    def add_to_blacklist(owner_id: int, members_list):
        Manager.check_none(owner_id=owner_id, members_list=members_list)
        for member in members_list:
            if UserManager.retrieve_by_id(member["id"]) is not None:
                entry = BlackList(owner=owner_id, member=member["id"])
                Manager.add_to_blacklist(entry)

    @staticmethod
    def delete_from_blacklist(owner_id: int, members_list):
        Manager.check_none(owner_id=owner_id, members_list=members_list)
        for member in members_list:
            if UserManager.retrieve_by_id(member["id"]) is not None:
                Manager.delete_member_from_blacklist(owner_id, member["id"])

    @staticmethod
    def get_blacklist_candidates(owner_id: int):
        Manager.check_none(owner_id=owner_id)
        candidates = Manager.get_blacklist_candidates(owner_id)
        return candidates

    @staticmethod
    def get_blacklisted(owner_id: int):
        Manager.check_none(owner_id=owner_id)
        blacklisted = Manager.get_blacklisted(owner_id)
        return blacklisted

    @staticmethod
    def report(user: User):
        Manager.check_none(user=user)
        setattr(user, "reports", user.reports + 1)
        # if the user has 3 or more reports ban the account deactivating it
        if user.reports >= 3:
            user.is_active = False
        Manager.commit()

    @staticmethod
    def set_content_filter(user: User, value: bool):
        Manager.check_none(user=user, value=value)
        setattr(user, "content_filter", value)
        Manager.commit()

    @staticmethod
    def unregister(user: User):
        Manager.check_none(user=user)
        setattr(user, "is_active", False)
        Manager.commit()

    @staticmethod
    def get_all_users():
        all_users = Manager.get_all_users()
        all_users = [user_dict(u) for u in all_users]
        return all_users

    @staticmethod
    def get_banned_users():
        banned = Manager.get_banned_users()
        banned = [user_dict(u) for u in banned]
        return banned

    @staticmethod
    def get_recipients(user_id: int):
        Manager.check_none(user_id=user_id)
        recipients = Manager.get_recipients(user_id)
        recipients = [{"id": u.id, "email": u.email} for u in recipients]
        return recipients

    @staticmethod
    def get_unregistered_users():
        unregistered_users = Manager.get_unregistered_users()
        unregistered_users = [user_dict(u) for u in unregistered_users]
        return unregistered_users

    @staticmethod
    def get_all_users_public():
        public_users = Manager.get_all_users_public()
        public_users = [user_public_dict(u) for u in public_users]
        return public_users


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
