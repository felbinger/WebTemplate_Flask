import json

from app.api import User, Role, Token
from .utils import _generate_default, \
    _create_role, _create_user, _generate_user_token, \
    _create_admin_role, _create_admin_user, _generate_admin_token, \
    _generate_named_role, _generate_named_user


def test_create_role(app, client):
    db = client.db
    with app.app_context():
        resp = client.post(
            '/api/roles',
            headers={'Access-Token': _generate_admin_token(app, client)},
            json={'name': 'test', 'description': 'desc'}
        )
        assert resp.status_code == 201
        assert json.loads(resp.data.decode()).get('data').get('description') == 'desc'


def test_create_role_without_data(app, client):
    db = client.db
    with app.app_context():
        resp = client.post(
            '/api/roles',
            headers={'Access-Token': _generate_admin_token(app, client)}
        )
        assert resp.status_code == 400
        assert json.loads(resp.data.decode()).get('message') == 'Payload is invalid'


def test_create_role_invalid_data(app, client):
    db = client.db
    with app.app_context():
        resp = client.post(
            '/api/roles',
            headers={'Access-Token': _generate_admin_token(app, client)},
            json={'invalid': 'invalid'}
        )
        assert resp.status_code == 400
        assert json.loads(resp.data.decode()).get('message') == 'Payload is invalid'


def test_get_all_roles(app, client):
    db = client.db
    with app.app_context():
        _generate_default(app, client)
        resp = client.get('/api/roles', headers={'Access-Token': _generate_admin_token(app, client)})
        assert resp.status_code == 200
        assert len(json.loads(resp.data.decode()).get('data')) == len(Role.query.all())


def test_get_role(app, client):
    db = client.db
    with app.app_context():
        _generate_default(app, client)
        resp = client.get(f'/api/roles/admin', headers={'Access-Token': _generate_admin_token(app, client)})
        assert resp.status_code == 200
        assert json.loads(resp.data.decode()).get('data').get('description') == "Administrator"


def test_get_invalid_role(app, client):
    db = client.db
    with app.app_context():
        _generate_default(app, client)
        resp = client.get(f'/api/roles/invalid', headers={'Access-Token': _generate_admin_token(app, client)})
        assert resp.status_code == 404
        assert json.loads(resp.data.decode()).get('message') == 'Role does not exist!'


def test_update_role(app, client):
    db = client.db
    with app.app_context():
        _generate_default(app, client)
        resp = client.put(
            '/api/roles/user',
            headers={'Access-Token': _generate_admin_token(app, client)},
            json={'description': 'new'}
        )
        assert resp.status_code == 200
        assert json.loads(resp.data.decode()).get('data').get('description') == 'new'


def test_update_invalid_role(app, client):
    db = client.db
    with app.app_context():
        _generate_default(app, client)
        resp = client.put(
            '/api/roles/invalid',
            headers={'Access-Token': _generate_admin_token(app, client)},
            json={'description': 'new'}
        )
        assert resp.status_code == 404
        assert json.loads(resp.data.decode()).get('message') == 'Role does not exist!'


def test_update_role_invalid_data(app, client):
    db = client.db
    with app.app_context():
        _generate_default(app, client)
        resp = client.put(
            '/api/roles/user',
            headers={'Access-Token': _generate_admin_token(app, client)},
            json={'invalid': 'invalid'}
        )
        assert resp.status_code == 400
        assert json.loads(resp.data.decode()).get('message') == 'Payload is invalid'


def test_delete_role(app, client):
    db = client.db
    with app.app_context():
        _generate_named_role(app, client, name='test')
        resp = client.delete(f'/api/roles/test', headers={'Access-Token': _generate_admin_token(app, client)})
        assert resp.status_code == 204

