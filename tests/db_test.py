import json
from uuid import UUID

from app.api import User, Role, Token
from .utils import _create_role, _create_user, _generate_user_token, \
    _create_admin_role, _create_admin_user, _generate_admin_token


def test_create_models(client):
    assert client.db is not None


def test_create_token(app, client):
    db = client.db
    with app.app_context():
        token = Token(
            user=_create_user(app, client)
        )
        db.session.add(token)
        db.session.commit()

        assert len(Token.query.all()) == 1
        assert Token.query.first().broken == 0
        assert len(UUID(Token.query.first().token).hex) == 32


def test_create_role(app, client):
    db = client.db
    with app.app_context():
        role = Role(
            name='admin',
            description='Administrator'
        )
        db.session.add(role)
        db.session.commit()

        assert len(Role.query.all()) == 1

        assert isinstance(Role.query.first(), Role)
        assert Role.query.first().name == 'admin'
        assert Role.query.first().description == 'Administrator'


def test_create_user(app, client):
    db = client.db
    with app.app_context():
        user = User(
            username='test',
            display_name='Testine Test',
            email='testine@test.de',
            password='PasswordForTestine',
            role=_create_role(app, client)
        )
        db.session.add(user)
        db.session.commit()

        assert len(User.query.all()) == 1

        assert isinstance(User.query.first(), User)
        assert len(UUID(User.query.first().public_id).hex) == 32
        assert User.query.first().verify_password('PasswordForTestine')
        assert User.query.first().username == 'test'
        assert User.query.first().display_name == 'Testine Test'
        assert User.query.first().email == 'testine@test.de'
