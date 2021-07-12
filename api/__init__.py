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
    description=(
        "<p>"
        "<strong>"
        "Flask / SQLAlchemy API containing wizard characters, potions and spells"
        "</strong>"
        "</p>"
        "<p>"
        "For using the protected endpoints, please register first with POST "
        "/register and get the Bearer access token or use POST /login to get the "
        "Bearer access token when you are already registered."
        "</p>"
    ),
    title="Wizard API",
    default="Endpoints",
    default_label=None,
    validate=True,
)
