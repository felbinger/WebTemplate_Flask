from flask.views import MethodView
from flask import request
from hashlib import sha512

from app.db import db
from ..schemas import ResultSchema, ResultErrorSchema
from ..authentication import Token, require_token, require_admin
from ..role import Role
from .models import User
from .schemas import DaoCreateUserSchema, DaoUpdateUserSchema


class UserResource(MethodView):
    """
    curl -H "Access-Token: $token" -X GET localhost:5000/api/users
    """
    @require_token
    @require_admin
    def get(self, uuid, **_):
        if uuid is None:
            # get all users
            return ResultSchema(
                data=[d.jsonify() for d in User.query.all()]
            ).jsonify()
        else:
            # get a user by the uuid in the resource (url)
            data = User.query.filter_by(public_id=uuid).first()
            if not data:
                return ResultErrorSchema(
                    message='User does not exist!',
                    errors=['user does not exist'],
                    status_code=404
                ).jsonify()
            return ResultSchema(
                data=data.jsonify()
            ).jsonify()

    """
    curl -X POST localhost:5000/api/users -H "Access-Token: $token" -H "Content-Type: application/json" \
    -d '{"username": "johndoe", "password": "JohnDoe2", "email": "john@doe.de", "role": "admin"}'
    """
    @require_token
    @require_admin
    def post(self, **_):
        schema = DaoCreateUserSchema()

        # check if the submitted data is correct
        data, error = schema.load(request.get_json() or {})
        if error:
            return ResultErrorSchema(
                message='Payload is invalid',
                errors=error,
                status_code=400
            ).jsonify()

        # check if username or email is already in use
        if User.query.filter((User.username == data['username']) | (User.email == data['email'])).first():
            return ResultErrorSchema(
                message='Username or email already in use!',
                errors=['username or email already in use'],
                status_code=422
            ).jsonify()

        # get the role object
        data['role'] = Role.query.filter_by(name=data.get('role')).first()

        # check
        if not data['role']:
            return ResultErrorSchema(
                message='Role does not exist!',
                errors=['role does not exist'],
                status_code=404
            ).jsonify()

        # create user object, add it to the database and commit the changes
        user = User(**data)
        db.session.add(user)
        db.session.commit()

        return ResultSchema(
            data=user.jsonify(),
            status_code=201
        ).jsonify()

    """
    curl -X PUT localhost:5000/api/users/89789fc7-4655-413d-8339-6fabedb1eab0 -H "Access-Token: $token" \
    -H "Content-Type: application/json" -d '{"email": "neue@mail.de"}'
    """
    @require_token
    def put(self, uuid, user, **_):
        if uuid == 'me':
            schema = DaoUpdateUserSchema()

            # check if the submitted data is correct
            data, error = schema.load(request.get_json())
            if error:
                return ResultErrorSchema(
                    message='Payload is invalid',
                    errors=error,
                    status_code=400
                ).jsonify()

            # check if the user is trying to change his role (not allowed)
            if 'role' in data.keys():
                return ResultErrorSchema(
                    message='You are not allowed to change your role!',
                    errors='not allowed to change role',
                    status_code=403
                ).jsonify()
            if 'username' in data.keys():
                return ResultErrorSchema(
                    message='You are not allowed to change your username!',
                    errors='not allowed to change username',
                    status_code=403
                ).jsonify()
            for key, val in data.items():
                if key == 'password':
                    setattr(user, key, sha512(val.encode()).hexdigest())
                else:
                    setattr(user, key, val)
            db.session.commit()
            return ResultSchema(
                data=user.jsonify()
            ).jsonify()
        else:
            # get the user object to update
            target = User.query.filter_by(public_id=uuid).first()
            if not target:
                return ResultErrorSchema(
                    message='User does not exist',
                    errors=['user does not exist'],
                    status_code=404
                ).jsonify()
            return require_admin(self._update_user_as_admin)(user=user, target=target)

    """
    curl -X DELETE localhost:5000/api/users/2a1c8ba8-f12e-4d2a-97c3-2fe454fefc6e -H "Access-Token: $token"
    curl -X DELETE localhost:5000/api/users/me -H "Access-Token: $token"
    """
    @require_token
    def delete(self, uuid, user, **_):
        if uuid == 'me':
            # delete all tokens for this user to prevent foreign key errors
            for token in Token.query.filter_by(user=user).all():
                db.session.delete(token)
            db.session.delete(user)
            db.session.commit()
            return ResultSchema(
                data='Successfully deleted user.',
                status_code=200
            ).jsonify()
        else:
            token = request.headers.get('Access-Token')
            if token:
                token_obj = Token.query.filter_by(token=token).first()
                if token_obj:
                    if not token_obj.is_valid() or not token_obj.user:
                        return ResultErrorSchema(
                            message='Invalid Access-Token',
                            errors=['invalid access token'],
                            status_code=401
                        ).jsonify()
                    else:
                        user = User.query.filter_by(public_id=uuid).first()
                        # delete all tokens for this user to prevent foreign key errors
                        for token in Token.query.filter_by(user=user).all():
                            db.session.delete(token)
                        db.session.delete(user)
                        db.session.commit()
                        return ResultSchema(
                            data='Successfully deleted user.',
                            status_code=200
                        ).jsonify()

    def _update_user_as_admin(self, target, **_):
        schema = DaoUpdateUserSchema()

        # check if the submitted data is correct
        data, error = schema.load(request.get_json())
        if error:
            return ResultErrorSchema(
                message='Payload is invalid',
                errors=error,
                status_code=400
            ).jsonify()

        # for each item in data
        for key, val in data.items():
            # check if the key need an special treatment
            # role need to be the role object, get the object and add it to the user
            if key == 'role':
                role = Role.query.filter_by(name=val).first()
                if not role:
                    return ResultErrorSchema(
                        message='Role does not exist!',
                        errors=['role does not exist'],
                        status_code=400
                    ).jsonify()
                else:
                    target.role = role
            # the password should be hashed
            elif key == 'password':
                setattr(target, key, sha512(val.encode()).hexdigest())
            else:
                # all others attributes can be added plain
                setattr(target, key, val)
        # commit changes
        db.session.commit()
        return ResultSchema(
            data=target.jsonify()
        ).jsonify()

