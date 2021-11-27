from mib import db
from mib.models.user import User, BlackList


class Manager(object):

    db_session = db.session

    @staticmethod
    def check_none(**kwargs):
        for name, arg in zip(kwargs.keys(), kwargs.values()):
            if arg is None:
                raise ValueError("You can't set %s argument to None" % name)

    @staticmethod
    def create(**kwargs):
        Manager.check_none(**kwargs)

        for bean in kwargs.values():
            db.session.add(bean)
        db.session.commit()

    @staticmethod
    def retrieve():
        """
        It should implemented by child
        :return:
        """
        pass

    @staticmethod
    def commit():
        db.session.commit()

    @staticmethod
    def update(**kwargs):
        Manager.check_none(**kwargs)
        db.session.commit()

    @staticmethod
    def delete(**kwargs):
        Manager.check_none(**kwargs)

        for bean in kwargs.values():
            db.session.delete(bean)
        db.session.commit()

    @staticmethod
    def add_to_blacklist(entry):
        db.session.add(entry)
        db.session.commit()

    @staticmethod
    def delete_member_from_blacklist(owner: int, member: int):
        db.session.query(BlackList).filter(BlackList.owner == owner).filter(
            BlackList.member == member
        ).delete()
        Manager.commit()

    @staticmethod
    def get_blacklist_candidates(owner_id: int):
        result = (
            db.session.query(User.id, User.email)
            .filter(User.id != owner_id, User.reports < 3, User.is_active)
            .filter(
                User.id.not_in(
                    db.session.query(BlackList.member).filter(
                        BlackList.owner == owner_id
                    )
                )
            )
            .all()
        )
        result = [(usr.id, usr.email) for usr in result]
        return result

    @staticmethod
    def get_blacklisted(owner_id: int):
        result = (
            db.session.query(BlackList.member, User.email)
            .filter(BlackList.owner == owner_id)
            .filter(BlackList.member == User.id)
            .all()
        )
        result = [(usr.id, usr.email) for usr in result]
        return result

    @staticmethod
    def get_all_users():
        result = db.session.query(User).filter(User.is_active).all()
        return result

    @staticmethod
    def get_banned_users():
        result = (
            db.session.query(User)
            .filter(User.is_active == False, User.reports >= 3)
            .all()
        )
        return result

    @staticmethod
    def get_recipients(user_id: int):
        result = (
            db.session.query(User.id, User.email)
            .filter(User.id != user_id, User.is_active)
            .filter(
                User.id.not_in(
                    db.session.query(BlackList.member).filter(
                        BlackList.owner == user_id
                    )
                )
            )
        )
        return result

    @staticmethod
    def get_unregistered_users():
        result = (
            db.session.query(User)
            .filter(User.is_active == False, User.reports < 3)
            .all()
        )
        return result

    @staticmethod
    def get_all_users_public():
        result = (
            db.session.query(User.email, User.firstname, User.lastname)
            .filter(User.is_active)
            .all()
        )
        return result
