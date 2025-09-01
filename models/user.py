"""
User model.

Defines a basic user record with username and email.  The global
`db` instance from `models.__init__` is used for the model base.
"""

from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"<User {self.username}>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }
