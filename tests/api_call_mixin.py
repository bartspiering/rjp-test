import json

from conftest import test_app
from model import db, User


class ApiCallMixin:
    def api_get(self, url: str, headers: dict = {}):
        with test_app().test_client() as test_client:
            return test_client.get(url, headers=headers)

    def api_post(self, url: str, payload: dict, headers: dict = {}):
        with test_app().test_client() as test_client:
            return test_client.post(
                url,
                data=json.dumps(payload),
                content_type="application/json",
                headers=headers,
            )

    def api_put(self, url: str, payload: dict, headers: dict = {}):
        with test_app().test_client() as test_client:
            return test_client.put(
                url,
                data=json.dumps(payload),
                content_type="application/json",
                headers=headers,
            )

    def api_delete(self, url: str, headers: dict = {}):
        with test_app().test_client() as test_client:
            return test_client.delete(url, headers=headers)

    @property
    def user_credentials(self):
        return {
            "email": "john.doe@gmail.com",
            "password": "Testtest1!",
        }

    @property
    def login_headers(self):
        json_data = json.loads(self.register().get_data())
        return {"Authorization": f"Bearer {json_data['access_token']}"}

    def register(self, user_credentials: dict = None, clean_up: bool = True):
        if clean_up:
            User.query.delete()
            db.session.commit()

        if user_credentials is None:
            user_credentials = self.user_credentials

        return self.api_post("/register", user_credentials)

    def login(self, user_credentials: dict = None):
        if user_credentials is None:
            user_credentials = self.user_credentials

        return self.api_post("/login", user_credentials)
