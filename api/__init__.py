from flask_restx import Api
from flask_jwt_extended import JWTManager


jwt = JWTManager()

api = Api(
    authorizations={
        "Bearer": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": (
                "Type in the *'Value'* input box below: "
                "**'Bearer &lt;JWT&gt;'**, where JWT is the token"
            ),
        }
    },
    validate=True,
)
