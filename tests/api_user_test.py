import json

from app.api import User, Role, Token
from .utils import _generate_default, \
    _create_role, _create_user, _generate_user_token, \
    _create_admin_role, _create_admin_user, _generate_admin_token, \
    _generate_named_role, _generate_named_user


def test_create_user(app, client):
    db = client.db
    with app.app_context():
        _generate_default(app, client)
        resp = client.post(
            '/api/users',
            headers={'Access-Token': _generate_admin_token(app, client)},
            json={
                'username': 'random',
                'email': 'ra@nd.om',
                'password': 'super_random',
                'role': 'user'
            }
        )
        assert resp.status_code == 201
        assert json.loads(resp.data.decode()).get('data').get('username') == 'random'


def test_create_user_invalid_role(app, client):
    db = client.db
    with app.app_context():
        resp = client.post(
            '/api/users',
            headers={'Access-Token': _generate_admin_token(app, client)},
            json={
                'username': 'random',
                'email': 'ra@nd.om',
                'password': 'super_random',
                'role': 'invalid'
            }
        )
        assert resp.status_code == 404
        assert json.loads(resp.data.decode()).get('message') == 'Role does not exist!'


def test_create_two_equal_users(app, client):
    db = client.db
    with app.app_context():
        _generate_default(app, client)
        resp = client.post(
            '/api/users',
            headers={'Access-Token': _generate_admin_token(app, client)},
            json={
                'username': 'random',
                'email': 'ra@nd.om',
                'password': 'super_random',
                'role': 'user'
            }
        )
        assert resp.status_code == 201
        resp = client.post(
            '/api/users',
            headers={'Access-Token': _generate_admin_token(app, client)},
            json={
                'username': 'random',
                'email': 'ra@nd.om',
                'password': 'super_random',
                'role': 'user'
            }
        )
        assert resp.status_code == 422
        assert json.loads(resp.data.decode()).get('message') == 'Username or email already in use!'


def test_create_user_without_data(app, client):
    db = client.db
    with app.app_context():
        resp = client.post('/api/users', headers={'Access-Token': _generate_admin_token(app, client)})
        assert resp.status_code == 400
        assert json.loads(resp.data.decode()).get('message') == 'Payload is invalid'


def test_create_user_invalid_data(app, client):
    db = client.db
    with app.app_context():
        resp = client.post(
            '/api/users',
            headers={'Access-Token': _generate_admin_token(app, client)},
            json={'invalid': 'invalid'}
        )
        assert resp.status_code == 400
        assert json.loads(resp.data.decode()).get('message') == 'Payload is invalid'


def test_get_all_user(app, client):
    db = client.db
    with app.app_context():
        _generate_default(app, client)
        _generate_named_user(app, client, name='random')
        resp = client.get('/api/users', headers={'Access-Token': _generate_admin_token(app, client)})
        assert resp.status_code == 200
        assert len(json.loads(resp.data.decode()).get('data')) == 2


def test_get_user(app, client):
    db = client.db
    with app.app_context():
        _generate_default(app, client)
        _generate_named_user(app, client, name='random')
        resp = client.get(
            f'/api/users/{str(User.query.filter_by(username="random").first().public_id)}',
            headers={'Access-Token': _generate_admin_token(app, client)}
        )
        assert resp.status_code == 200
        assert json.loads(resp.data.decode()).get('data').get('username') == 'random'


def test_get_invalid_user(app, client):
    db = client.db
    with app.app_context():
        resp = client.get(f'/api/users/invalid', headers={'Access-Token': _generate_admin_token(app, client)})
        assert resp.status_code == 404
        assert json.loads(resp.data.decode()).get('message') == 'User does not exist!'


def test_self_update(app, client):
    db = client.db
    with app.app_context():
        resp = client.put(
            '/api/users/me',
            headers={'Access-Token': _generate_user_token(app, client)},
            json={'displayName': 'Jane Doe'}
        )
        assert resp.status_code == 200
        assert json.loads(resp.data.decode()).get('data').get('displayName') == 'Jane Doe'


def test_self_update_change_role_unauthorized(app, client):
    db = client.db
    with app.app_context():
        resp = client.put(
            '/api/users/me',
            headers={'Access-Token': _generate_user_token(app, client)},
            json={'role': 'admin'}
        )
        assert resp.status_code == 403
        assert json.loads(resp.data.decode()).get('message') == 'You are not allowed to change your role!'


def test_admin_update(app, client):
    db = client.db
    with app.app_context():
        _generate_named_user(app, client, name='random')
        resp = client.put(
            f'/api/users/{str(User.query.filter_by(username="random").first().public_id)}',
            headers={'Access-Token': _generate_admin_token(app, client)},
            json={'role': 'admin'}
        )
        assert resp.status_code == 200
        assert json.loads(resp.data.decode()).get('data').get('role').get('description') == 'Administrator'


def test_admin_update_invalid_user(app, client):
    db = client.db
    with app.app_context():
        _generate_named_user(app, client, name='random')
        resp = client.put(
            '/api/users/invalid',
            headers={'Access-Token': _generate_admin_token(app, client)},
            json={'role': 'admin'}
        )
        assert resp.status_code == 404
        assert json.loads(resp.data.decode()).get('message') == 'User does not exist'


def test_admin_update_invalid_data(app, client):
    db = client.db
    with app.app_context():
        _generate_named_user(app, client, name='random')
        resp = client.put(
            f'/api/users/{str(User.query.filter_by(username="random").first().public_id)}',
            headers={'Access-Token': _generate_admin_token(app, client)},
            json={'invalid': 'invalid'}
        )
        # wont give out an error, because it does not care about invalid key's
        assert resp.status_code == 200


def test_self_delete(app, client):
    db = client.db
    with app.app_context():
        resp = client.delete('/api/users/me', headers={'Access-Token': _generate_user_token(app, client)})
        assert resp.status_code == 204


def test_delete_user(app, client):
    db = client.db
    with app.app_context():
        _generate_named_user(app, client, name='random')
        resp = client.delete(
            f'/api/users/{str(User.query.filter_by(username="random").first().public_id)}',
            headers={'Access-Token': _generate_admin_token(app, client)}
        )
        assert resp.status_code == 204
