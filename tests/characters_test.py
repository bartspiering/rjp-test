import json
import unittest

from tests.api_call_mixin import ApiCallMixin


class CharactersTest(unittest.TestCase, ApiCallMixin):
    def test_crud(self):
        headers = self.login_headers

        payload = {
            "name": "Albus Percival Wulfric Brian Dumbledore",
            "gender": "Male",
            "job": "Headmaster",
            "house": "Gryffindor",
            "wand": '15" Elder Thestral tail hair core',
            "patronus": "Phoenix",
            "species": "Human",
            "blood_status": "Half-blood",
            "hair_colour": "Silver| formerly auburn",
            "eye_colour": "Blue",
            "loyalty": "Dumbledore's Army | Order of the Phoenix | Hogwarts School of Witchcraft and Wizardry",
            "skills": "Considered by many to be one of the most powerful wizards of his time",
            "birth": "Late August 1881",
            "death": "30 June, 1997",
        }

        # test post with bad payload
        response = self.api_post("/characters", {}, headers)

        self.assertEqual(response.status_code, 400)

        # test proper post
        response = self.api_post("/characters", payload, headers)

        self.assertEqual(response.status_code, 201)

        json_data = json.loads(response.get_data())

        for key, value in payload.items():
            self.assertEqual(value, json_data[key])

        # test put
        payload["species"] = "Alien"

        response = self.api_put(f"/characters/{json_data['id']}", payload, headers)

        json_data = json.loads(response.get_data())

        self.assertEqual(response.status_code, 200)

        for key, value in payload.items():
            self.assertEqual(value, json_data[key])

        # test delete
        response = self.api_delete(f"/characters/{json_data['id']}", headers)

        self.assertEqual(response.status_code, 204)

        # test if delete worked
        response = self.api_get(f"/characters/{json_data['id']}", headers)

        self.assertEqual(response.status_code, 404)
