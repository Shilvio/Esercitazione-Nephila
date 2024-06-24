from rest_framework.test import APITestCase

class TestAuth(APITestCase):

    utente = {
            "username": "test",
            "password": "test",
            "ruolo": 0
            }

    user_bad_data = {
            "username": "test",
            "password": "test",
            "ruolo": 20
            }

    login_user = {
            "username": "test",
            "password": "test",
            }

    def setUp(self):
        self.register_url = 'http://127.0.0.1:8000/register'
        self.login_url = 'http://127.0.0.1:8000/login'


        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_register_no_data(self):
        response=self.client.post(self.register_url)
        self.assertEqual(response.status_code,400)

    def test_register_ok(self):
        response=self.client.post(path=self.register_url,data=self.utente, format='json')
        self.assertEqual(response.status_code,201)

    def test_register_bad_data(self):
        response=self.client.post(path=self.register_url,data=self.user_bad_data, format='json')
        self.assertEqual(response.status_code,400)

    def test_login_ok(self):
        self.client.post(path=self.register_url,data=self.utente, format='json')
        response=self.client.post(path=self.login_url,data=self.login_user, format='json')
        self.assertEqual(response.status_code,201)

    def test_register_no_data(self):
        response=self.client.post(self.register_url)
        self.assertEqual(response.status_code,400)