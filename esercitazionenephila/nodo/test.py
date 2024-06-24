from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

class TestAuth(APITestCase):

    utente = {
            "username": "test",
            "password": "test",
            "ruolo": 0
            }

    nodo = {
        "titolo": "titolo test"
    }

    nodo_bad_data = {
        "bad_data": "titolo test"
    }

    def setUp(self):
        self.register_url = 'http://127.0.0.1:8000/register'
        self.nodo_root = 'http://127.0.0.1:8000/nodi'
        self.nodo_creato = 'http://127.0.0.1:8000/nodi/1'
        self.nodo_inesistente = 'http://127.0.0.1:8000/nodi/2'
        self.nodo_padre = 'http://127.0.0.1:8000/nodi/padre'
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    # autentica utente
    def authenticate(self):
        self.client.post(path=self.register_url,data=self.utente, format='json')
        token = Token.objects.get(user__username=self.utente['username'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    # test condizioni ottimali
    def test_post_nodo_ok(self):
        self.authenticate()
        response = self.client.post(path=self.nodo_root,data=self.nodo, format='json')
        self.assertEqual(response.status_code,201)

    # test post nodo radice utente non autenticato
    def test_post_nodo_not_authenticated(self):
        response = self.client.post(path=self.nodo_root,data=self.nodo, format='json')
        self.assertEqual(response.status_code,403)

    # test post nodo radice senza dati nel body
    def test_post_nodo_no_data(self):
        self.authenticate()
        response = self.client.post(path=self.nodo_root, format='json')
        self.assertEqual(response.status_code,400)

    # test post nodo radice, con dati sporchi nel body
    def test_post_nodo_bad_data(self):
        self.authenticate()
        response = self.client.post(path=self.nodo_root,data=self.nodo_bad_data, format='json')
        self.assertEqual(response.status_code,400)

    # test get nodo condizioni ottimali
    def test_get_nodo_ok(self):
        self.test_post_nodo_ok()
        response = self.client.get(path=self.nodo_creato, format='json')
        self.assertEqual(response.status_code,200)

    # test get nodo condizioni utente non autenticato
    def test_get_nodo_ok(self):
        self.test_post_nodo_ok()
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.get(path=self.nodo_creato, format='json')
        self.assertEqual(response.status_code,403)

    # test get nodo con url avente nodo inesistente
    def test_get_nodo_bad_url(self):
        self.test_post_nodo_ok()
        response = self.client.get(path=self.nodo_inesistente, format='json')
        self.assertEqual(response.status_code,404)

    # test put nodo condizioni ottimali
    def test_put_nodo_ok(self):
        self.test_post_nodo_ok()
        response = self.client.put(path=self.nodo_creato,data=self.nodo, format='json')
        self.assertEqual(response.status_code,200)

    # test put nodo senza dati nel body
    def test_put_nodo_no_data(self):
        self.test_post_nodo_ok()
        response = self.client.put(path=self.nodo_creato, format='json')
        self.assertEqual(response.status_code,400)

    # test put con url avente nodo inesistente
    def test_put_nodo_bad_url(self):
        self.test_post_nodo_ok()
        response = self.client.put(path=self.nodo_inesistente, format='json')
        self.assertEqual(response.status_code,400)

    # test put nodo condizioni ottimali
    def test_put_nodo_bad_data(self):
        self.test_post_nodo_ok()
        response = self.client.put(path=self.nodo_creato,data=self.nodo, format='json')
        self.assertEqual(response.status_code,200)
