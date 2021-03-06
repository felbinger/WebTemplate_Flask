from marshmallow import Schema, fields, validate
from flask import jsonify

from ..schemas import validate_spaces


class AuthSchema(Schema):
    username = fields.Str(
        required=True,
        validate=[validate.Length(min=1, max=200), validate_spaces]
    )
    password = fields.Str(
        required=True,
        validate=[validate.Length(min=1, max=200)]
    )


class AuthResultSchema:
    __slots__ = ['message', 'errors', 'token', 'status_code']

    def __init__(self, message, errors=None, token=None, status_code=200):
        self.message = message
        self.errors = errors or []
        self.token = token
        self.status_code = status_code

    def jsonify(self):
        return jsonify({
            'message': self.message,
            'errors': self.errors,
            'token': self.token,
            'statusCode': self.status_code
        }), self.status_code
