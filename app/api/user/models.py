from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from uuid import uuid4
from hashlib import sha512
from datetime import datetime
from random import SystemRandom
from string import ascii_lowercase, ascii_uppercase, digits
from flask import current_app

from app.db import db


class User(db.Model):
    __table_args__ = ({'mysql_character_set': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_520_ci'})
    id = Column('id', Integer, primary_key=True)
    public_id = Column('publicId', String(36), unique=True, nullable=False)
    username = Column('username', String(100), unique=True, nullable=False)
    display_name = Column('displayName', String(100))
    email = Column('email', String(100), unique=True, nullable=False)
    salt = Column('salt', String(128), nullable=False)
    password = Column('password', String(255), nullable=False)
    created = Column('created', DateTime, nullable=False)
    last_login = Column('lastLogin', DateTime)

    role_id = Column('role', Integer, ForeignKey('role.id'), nullable=False)
    role = db.relationship('Role', backref=db.backref('users', lazy=True))

    def __init__(self, *args, **kwargs):
        self.salt = User._generate_salt(length=current_app.config['SALT_LENGTH'])
        kwargs['password'] = sha512(self.salt.encode() + kwargs['password'].encode()).hexdigest()
        super().__init__(*args, **kwargs, public_id=str(uuid4()), created=datetime.utcnow())

    @staticmethod
    def _generate_salt(length=12, chars=ascii_lowercase + ascii_uppercase + digits):
            return ''.join(SystemRandom().choice(chars) for _ in range(length))

    def min_jsonify(self):
        return {
            # return the display name if it has been set else return the username
            'name': self.username if not self.display_name else self.display_name,
            'role': self.role
        }

    def jsonify(self):
        return {
            'publicId': self.public_id,
            'username': self.username,
            'displayName': self.display_name,
            'email': self.email,
            'created': self.created.isoformat(),
            'lastLogin': self.last_login.isoformat() if self.last_login else None,
            'role': self.role.jsonify()
        }

    def verify_password(self, password):
        return self.password == sha512(self.salt.encode() + password.encode()).hexdigest()
