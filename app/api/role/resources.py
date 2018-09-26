from flask import request
from flask.views import MethodView

from app.db import db
from ..user import User
from ..authentication import require_token, require_admin
from ..schemas import ResultSchema, ResultErrorSchema
from .models import Role
from .schemas import DaoCreateRoleSchema, DaoUpdateRoleSchema


class RoleResource(MethodView):
    """
    curl -H "Access-Token: $token" -X GET localhost:5000/api/roles
    """
    @require_token
    def get(self, name, **_):
        if name is None:
            # get all roles
            return ResultSchema(
                data=[d.jsonify() for d in Role.query.all()]
            ).jsonify()
        else:
            # get a role by the name in the resource (url)
            role = Role.query.filter_by(name=name).first()
            if not role:
                return ResultErrorSchema(
                    message='Role does not exist!',
                    errors=['role does not exist'],
                    status_code=404
                ).jsonify()
            return ResultSchema(
                data=role.jsonify() or None
            ).jsonify()

    """
    curl -H "Access-Token: $token" -X POST localhost:5000/api/roles -H "Content-Type: application/json" \
    -d '{"name": "test", "description": "Test"}'
    """
    @require_token
    @require_admin
    def post(self, **_):
        schema = DaoCreateRoleSchema()

        # check if the submitted data is correct
        data, error = schema.load(request.get_json() or {})
        if error:
            return ResultErrorSchema(
                message='Payload is invalid',
                errors=error,
                status_code=400
            ).jsonify()

        # check if the name is already in use
        if Role.query.filter_by(name=data.get('name')).first():
            return ResultErrorSchema(
                message='Name already in use!',
                errors=['name already in use'],
                status_code=400
            ).jsonify()

        # create role object
        role = Role(
            name=data.get('name'),
            description=data.get('description')
        )

        # add role object to database and commit changes
        db.session.add(role)
        db.session.commit()
        return ResultSchema(
            data=role.jsonify(),
            status_code=201
        ).jsonify()

    """
    curl -H "Access-Token: $token" -X PUT localhost:5000/api/roles/test -H "Content-Type: application/json" \
    -d '{"description": "Test2"}'
    """
    @require_token
    @require_admin
    def put(self, name, **_):
        schema = DaoUpdateRoleSchema()

        # check if the submitted data is correct
        data, error = schema.load(request.get_json() or {})
        if error:
            return ResultErrorSchema(
                message='Payload is invalid',
                errors=error,
                status_code=400
            ).jsonify()

        # get the role object by the name
        role = Role.query.filter_by(name=name).first()

        # check if the role exist
        if not role:
            return ResultErrorSchema(
                message='Role does not exist!',
                errors=['role does not exist'],
                status_code=404
            ).jsonify()

        # update the description
        role.description = data.get('description')
        db.session.commit()
        return ResultSchema(
            data=role.jsonify()
        ).jsonify()

    """
    curl -v -H "Access-Token: $token" -X DELETE localhost:5000/api/roles/test
    """
    @require_token
    @require_admin
    def delete(self, name, **_):
        # Prevent deletion of required roles.
        if name == 'admin':
            return ResultErrorSchema(
                message='Admin role cannot be deleted!',
                errors=['admin role cannot be deleted'],
                status_code=422
            ).jsonify()
        if name == 'user':
            return ResultErrorSchema(
                message='User role cannot be deleted!',
                errors=['User role cannot be deleted'],
                status_code=422
            ).jsonify()

        # get the role object by the name
        role = Role.query.filter_by(name=name).first()

        # check if the role exist
        if not role:
            return ResultErrorSchema(
                message='Role does not exist!',
                errors=['role does not exist'],
                status_code=404
            ).jsonify()

        # check if an user has this role
        for user in User.query.all():
            if user.role == role:
                return ResultErrorSchema(
                    message='Role is in use!',
                    errors=['role is in use'],
                    status_code=422
                ).jsonify()
        db.session.delete(role)
        db.session.commit()
        return '', 204
