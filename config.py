import os


class Config(object):
    DEBUG = False
    TESTING = False

    PROPAGATE_EXCEPTIONS = True

    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{os.path.dirname(os.path.abspath(__file__))}/database/wizards.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 24
    JWT_SECRET_KEY = "change-me"

    BUNDLE_ERRORS = True
    RESTX_MASK_SWAGGER = False
    RESTX_VALIDATE = True


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{os.path.dirname(os.path.abspath(__file__))}/database/test.db"
    )
