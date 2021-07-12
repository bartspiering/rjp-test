import json
import unittest

from tests.api_call_mixin import ApiCallMixin


class AuthenticationTest(unittest.TestCase, ApiCallMixin):
    def test_registration(self):
        user_credentials_with_bad_email = self.user_credentials
        user_credentials_with_bad_email["email"] = user_credentials_with_bad_email[
            "email"
        ].replace("@", "")

        response = self.register(user_credentials_with_bad_email)

        self.assertEqual(response.status_code, 400)

        user_credentials_with_bad_password = self.user_credentials
        user_credentials_with_bad_password[
            "password"
        ] = user_credentials_with_bad_password["password"].replace("1!", "")

        response = self.register(user_credentials_with_bad_password)

        self.assertEqual(response.status_code, 400)

        response = self.register({})

        self.assertEqual(response.status_code, 400)

        response = self.register()

        self.assertEqual(response.status_code, 201)
        self.assertIn("access_token", json.loads(response.get_data()))

        response = self.register(clean_up=False)

        self.assertEqual(response.status_code, 409)

    def test_login(self):
        self.register()

        user_credentials_with_bad_email = self.user_credentials
        user_credentials_with_bad_email["email"] = user_credentials_with_bad_email[
            "email"
        ].replace("@", "")

        response = self.login(user_credentials_with_bad_email)

        self.assertEqual(response.status_code, 400)

        user_credentials_with_bad_password = self.user_credentials
        user_credentials_with_bad_password[
            "password"
        ] = user_credentials_with_bad_password["password"].replace("1!", "")

        response = self.login(user_credentials_with_bad_password)

        self.assertEqual(response.status_code, 403)

        response = self.login({})

        self.assertEqual(response.status_code, 400)

        response = self.login()

        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", json.loads(response.get_data()))
