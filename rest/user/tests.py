from urllib import response
from rest.tests import BaseTestCase

# Create your tests here.

class UserTest(BaseTestCase):

    def test_user_registration(self):
        client = self.unauthorized_call()
        endpoint = '/rest/users/sign-up/'
        payload = {
            'email':"jefri@gmai.com",
            'username':'jefri',
            'password':'Power3321'
        }
        response = client.post(endpoint, data=payload, headers=self.headers)
        assert(response.status_code == 201)

    def test_user_login(self):
        self.test_user_registration()
        payload = {
            'email':"jefri@gmai.com",
            'password':'Power3321'
        }
        endpoint = '/rest/users/login/'
        client = self.unauthorized_call()
        response = client.post(endpoint, data=payload, headers=self.headers)
        assert(response.status_code == 200)
        return response.json()

    def test_change_password(self):
        user = self.test_user_login()
        token = user['data']['token']
        client = self.authorized_call(token=token)
        payload = {
            "old_password": "Power3321",
            "new_password": "NewPassword3321"
        }
        endpoint = '/rest/users/password/change/'
        response = client.post(endpoint, data=payload, headers=self.headers)
        