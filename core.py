from flask import Flask
import flask_jwt_extended

from model import db
from api import api as api_app, jwt
from api.pagination import pagination


def create_app(config_name="DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(f"config.{config_name}")

    db.init_app(app)

    api_app.init_app(app)

    jwt.init_app(app)

    pagination.init_app(app, db)

    @app.errorhandler(flask_jwt_extended.exceptions.NoAuthorizationError)
    def handle_no_authorization_error(e):
        return {"message": str(e)}, 401

    import api.endpoints

    return app
