from sqlalchemy_utils import EmailType, PasswordType

from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(EmailType, nullable=False, unique=True)
    password = db.Column(PasswordType(schemes=["pbkdf2_sha512"]))
