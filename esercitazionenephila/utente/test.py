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
    login_user_bad_data = {
            "badData": "test",
            }


    def setUp(self):
        self.register_url = 'http://127.0.0.1:8000/register'
        self.login_url = 'http://127.0.0.1:8000/login'


        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    # test registrazione no dati
    def test_register_no_data(self):
        response=self.client.post(self.register_url)
        self.assertEqual(response.status_code,400)

    # test registrazione ideale
    def test_register_ok(self):
        response=self.client.post(path=self.register_url,data=self.utente, format='json')
        self.assertEqual(response.status_code,201)

    # test registrazione dati incompatibili
    def test_register_bad_data(self):
        response=self.client.post(path=self.register_url,data=self.user_bad_data, format='json')
        self.assertEqual(response.status_code,400)

    # test login ideale
    def test_login_ok(self):
        self.client.post(path=self.register_url,data=self.utente, format='json')
        response=self.client.post(path=self.login_url,data=self.login_user, format='json')
        self.assertEqual(response.status_code,201)

    # test login no utente in db
    def test_login_ok(self):
        response=self.client.post(path=self.login_url,data=self.login_user, format='json')
        self.assertEqual(response.status_code,404)

    # test login no dati
    def test_login_no_data(self):
        self.client.post(path=self.register_url, format='json')
        response=self.client.post(path=self.login_url, format='json')
        self.assertEqual(response.status_code,400)

    # test login dati malformati
    def test_login_bad_data(self):
        self.client.post(path=self.register_url, format='json')
        response=self.client.post(path=self.login_url,data=self.login_user_bad_data, format='json')
        self.assertEqual(response.status_code,400)


