"""User models."""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from webapp.db import db


class User(db.Model, UserMixin):
    """User models."""

    id = db.Column(db.Integer, primary_key=True)  # noqa: WPS125
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)
    email = db.Column(db.String(50))
    fns_login = db.Column(db.String(12))
    fns_password = db.Column(db.String(128))

    def __repr__(self):
        return f'<User {self.username}'

    def set_password(self, password):
        """Generate password hash."""
        self.password = generate_password_hash(password)  # noqa: WPS601

    def check_password(self, password):
        """Check password hash."""
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        """Is admin."""
        return self.role == 'admin'
