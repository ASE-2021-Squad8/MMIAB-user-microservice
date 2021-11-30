from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql.schema import ForeignKey
from dataclasses import dataclass
from mib import db


@dataclass
class User(db.Model):
    """Representation of User model."""

    # The name of the table that we explicitly set
    __tablename__ = "User"

    # A list of fields to be serialized
    SERIALIZE_LIST = ["id", "email", "is_active", "authenticated", "is_anonymous"]

    # All fields of user
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Unicode(128), nullable=False, unique=True)
    firstname = db.Column(db.Unicode(128), nullable=False, unique=False)
    lastname = db.Column(db.Unicode(128), nullable=False, unique=False)
    password = db.Column(db.Unicode(128))
    dateofbirth = db.Column(db.Date())
    reports = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    points = db.Column(db.Integer, default=0)
    content_filter = db.Column(db.Boolean, default=False)
    authenticated = db.Column(db.Boolean, default=True)
    is_anonymous = False

    def __init__(self, *args, **kw):
        super(User, self).__init__(*args, **kw)
        self.authenticated = False

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def set_email(self, email):
        self.email = email

    def set_firstname(self, name):
        self.firstname = name

    def set_lastname(self, name):
        self.lastname = name

    def set_dateofbirth(self, dateofbirth):
        self.dateofbirth = dateofbirth

    def authenticate(self, password):
        checked = check_password_hash(self.password, password)
        self.authenticated = checked
        return self.authenticated

    def serialize(self):
        return dict([(k, self.__getattribute__(k)) for k in self.SERIALIZE_LIST])


@dataclass
class BlackList(db.Model):
    """A user's blacklist"""

    __tablename__ = "blacklist"

    owner: int
    member: int

    # one blacklist per user
    owner = db.Column(db.Integer, ForeignKey(User.id), primary_key=True)
    member = db.Column(db.Integer, ForeignKey(User.id), primary_key=True)
