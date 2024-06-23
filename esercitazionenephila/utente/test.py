from rest_framework.test import APITestCase
from django.urls import reverse

class AuthTest(APITestCase):

    user = {
            "username": "test",
            "password": "test",
            "ruolo": 0
        }

    user_bad_data = {
        "username": "test",
        "password": "test",
        "ruolo": 20
    }

    def set_up(self):
        self.registerUrl = 'http://127.0.0.1:8000/register/'
        self.loginUrl = 'http://127.0.0.1:8000/login/'


        return super().setUp()

    def tear_down(self):
        return super().tearDown()

    def test_register_no_data(self):
        response=self.client.post(self.registerUrl)
        self.assertEqual(response.status_code,400)

    def test_register_ok(self):
        response=self.client.post(path=self.registerUrl,data=self.user, format='json')

        self.assertEqual(response.status_code,201)

    def test_register_bad_data(self):
        response=self.client.post(path=self.registerUrl,data=self.user_bad_data, format='json')
        self.assertEqual(response.status_code,400)