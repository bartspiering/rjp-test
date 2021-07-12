import os
import pytest

from core import create_app
from setup import run_setup


class TestAppInitializer:
    __app = None

    @property
    def app(self):
        if self.__app is not None:
            return self.__app

        self.__app = create_app("TestingConfig")
        self.__app.app_context().push()

        return self.__app


test_app_initializer = TestAppInitializer()


def test_app():
    return test_app_initializer.app


@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown():
    test_app_instance = test_app_initializer.app

    database_file = test_app_instance.config["SQLALCHEMY_DATABASE_URI"].replace(
        "sqlite://", ""
    )

    if os.path.exists(database_file):
        os.remove(database_file)

    run_setup("TestingConfig")

    yield

    os.remove(database_file)
