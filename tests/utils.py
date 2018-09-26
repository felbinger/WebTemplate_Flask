from app.api import User, Role, Token
import json


# Method to create the default rows in the database
def _generate_default(app, client):
    db = client.db
    with app.app_context():
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(
                name='admin',
                description='Administrator'
            )
            db.session.add(admin_role)
        user_role = Role.query.filter_by(name='user').first()
        if not user_role:
            user_role = Role(
                name='user',
                description='User'
            )
            db.session.add(user_role)
        db.session.commit()


# create a non admin role
def _create_role(app, client):
    db = client.db
    with app.app_context():
        _generate_default(app, client)
        role = Role.query.filter_by(name='user').first()
        if not role:
            role = Role(
                name='user',
                description='User'
            )
            db.session.add(role)
            db.session.commit()
        return role


# create an non admin user
def _create_user(app, client):
    db = client.db
    with app.app_context():
        user = User.query.filter_by(username='max').first()
        if not user:
            user = User(
                username='max',
                display_name='Max Mustermann',
                email='max@mustermann.de',
                password='PasswordForMax',
                role=_create_role(app, client)
            )
            db.session.add(user)
            db.session.commit()
        return user


# generate a token for an non admin user
def _generate_user_token(app, client):
    db = client.db
    with app.app_context():
        _generate_default(app, client)
        _create_user(app, client)
        resp = client.post('/api/auth', json={'username': 'max', 'password': 'PasswordForMax'})
        data = json.loads(resp.data.decode())
        return data.get('token')


# generate role by name
def _generate_named_role(app, client, name):
    db = client.db
    with app.app_context():
        _generate_default(app, client)
        role = Role.query.filter_by(name=name).first()
        if not role:
            role = Role(
                name=name,
                description='random'
            )
            db.session.add(role)
            db.session.commit()
        return role


# generate user by name
def _generate_named_user(app, client, name):
    db = client.db
    with app.app_context():
        user = User(
            username=name,
            display_name='random',
            email='ra@nd.om',
            password='random',
            role=_create_role(app, client)
        )
        db.session.add(user)
        db.session.commit()
        return user


# create the admin role
def _create_admin_role(app, client):
    db = client.db
    with app.app_context():
        _generate_default(app, client)
        role = Role.query.filter_by(name='admin').first()
        if not role:
            role = Role(
                name='admin',
                description='Administrator'
            )
            db.session.add(role)
            db.session.commit()
        return role


# create an admin user
def _create_admin_user(app, client):
    db = client.db
    with app.app_context():
        user = User.query.filter_by(username='test').first()
        if not user:
            user = User(
                username='test',
                display_name='Testine Test',
                email='testine@test.de',
                password='PasswordForTestine',
                role=_create_admin_role(app, client)
            )
            db.session.add(user)
            db.session.commit()
        return user


# generate a token for an admin user
def _generate_admin_token(app, client):
    db = client.db
    with app.app_context():
        _generate_default(app, client)
        _create_admin_user(app, client)
        resp = client.post('/api/auth', json={'username': 'test', 'password': 'PasswordForTestine'})
        data = json.loads(resp.data.decode())
        return data.get('token')
