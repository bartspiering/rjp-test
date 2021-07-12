from flask import abort
from flask_restx import Resource, fields, inputs
from flask_restx.reqparse import RequestParser
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError

from .. import api
from model import db, User
from ..reqparser.types import strong_password


register_request_fields = api.model(
    "RegisterRequest", {"email": fields.String, "password": fields.String}
)

register_request_parser = RequestParser()
register_request_parser.add_argument("email", required=True, type=inputs.email())
register_request_parser.add_argument("password", required=True, type=strong_password)

register_response_fields = api.model(
    "RegisterResponse", {"access_token": fields.String}
)


@api.route("/register")
class RegisterResource(Resource):
    @api.expect(register_request_fields)
    @api.marshal_with(register_response_fields, code=201, description="User created")
    @api.response(400, "Invalid input")
    @api.response(409, "User already exists")
    def post(self):
        args = register_request_parser.parse_args()

        user = User(**args)

        db.session.add(user)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(409, "User already exists")

        return {"access_token": create_access_token(identity=args["email"])}, 201
