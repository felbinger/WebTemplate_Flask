from .utils import _create_user, _generate_user_session


def test_login(app, client):
    db = client.db
    with app.app_context():
        _create_user(app, client)
        resp = client.post('/login', data={'username': 'max', 'password': 'PasswordForMax'})
        assert resp.status_code == 302  # expect redirect to another page
        assert 'session=' in resp.headers['Set-Cookie']


# TODO not working
def test_logout(app, client):
    db = client.db
    with app.app_context():
        resp = client.get('/logout', headers={'Cookie': _generate_user_session(app, client)})
        assert resp.status_code == 302  # expect redirect to another page
        print(resp.data)
