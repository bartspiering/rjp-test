from flask import abort
from flask_restx import Resource, fields, inputs
from flask_restx.reqparse import RequestParser
from flask_jwt_extended import create_access_token

from .. import api
from model import User


login_request_fields = api.model(
    "LoginRequest", {"email": fields.String, "password": fields.String}
)

login_request_parser = RequestParser()
login_request_parser.add_argument("email", required=True, type=inputs.email())
login_request_parser.add_argument("password")

login_response_fields = api.model("LoginResponse", {"access_token": fields.String})


@api.route("/login")
class LoginResource(Resource):
    @api.expect(login_request_fields)
    @api.marshal_with(login_response_fields, code=200, description="Login successful")
    @api.response(400, "Invalid input")
    @api.response(403, "Access denied")
    @api.response(404, "User not found")
    def post(self):
        args = login_request_parser.parse_args()

        user = User.query.filter(User.email == args["email"]).first_or_404(
            description="User not found"
        )

        if user.password != args["password"]:
            abort(403, "Access denied")

        return {"access_token": create_access_token(identity=user.email)}
