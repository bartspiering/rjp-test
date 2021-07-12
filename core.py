from flask import Flask

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

    import api.endpoints

    return app
