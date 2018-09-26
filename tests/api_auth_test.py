import json
from uuid import UUID
from dateutil import parser
from flask import Flask

from app.api import User, Role, Token
from app.api.authentication import require_admin
from .utils import _create_role, _create_user, _generate_user_token, \
    _create_admin_role, _create_admin_user, _generate_admin_token


def test_auth(app, client):
    db = client.db
    with app.app_context():
        _create_user(app, client)
        resp = client.post('/api/auth', json={'username': 'max', 'password': 'PasswordForMax'})
        print(resp.data)
        assert resp.status_code == 200
        assert len(json.loads(resp.data.decode()).get('errors')) == 0
        assert 'token' in json.loads(resp.data.decode())


def test_auth_without_data(app, client):
    db = client.db
    with app.app_context():
        resp = client.post('/api/auth')
        assert resp.status_code == 400
        assert json.loads(resp.data.decode()).get('message') == 'Payload is invalid'


def test_auth_invalid_data(app, client):
    db = client.db
    with app.app_context():
        resp = client.post('/api/auth', json={'username': 'invalid', 'password': 'invalid'})
        assert resp.status_code == 401
        assert json.loads(resp.data.decode()).get('message') == 'Wrong credentials'


def test_auth_get_user_data(app, client):
    db = client.db
    with app.app_context():
        resp = client.get('/api/auth', headers={'Access-Token': _generate_user_token(app, client)})
        assert resp.status_code == 200
        assert 'username' in json.loads(resp.data.decode()).get('data')
        assert parser.parse(json.loads(resp.data.decode()).get('data').get('created'))


def test_auth_get_user_data_without_token(app, client):
    db = client.db
    with app.app_context():
        resp = client.get('/api/auth')
        assert resp.status_code == 401
        assert json.loads(resp.data.decode()).get('message') == 'Missing Access-Token'


def test_auth_invalid_token(app, client):
    db = client.db
    with app.app_context():
        resp = client.get('/api/auth', headers={'Access-Token': 'invalid'})
        assert resp.status_code == 401
        assert json.loads(resp.data.decode()).get('message') == 'Invalid Access-Token'


def test_require_admin_error():
    app = Flask(__name__)

    @app.route('/')
    @require_admin
    def index(): pass
    client = app.test_client()
    resp = client.get('/')
    assert resp.status_code == 500
