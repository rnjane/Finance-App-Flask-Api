from tests import FinanceAppTestSetup
import json

class AuthTests(FinanceAppTestSetup):
    """User registration and login functionality tests"""

    def test_user_register_works(self):
        response = self.app.post('/register', data=json.dumps(dict(
                username='testuser1',
                email="test@test.com",
                password1='123456',
                password2='123456'
            )),
            content_type='application/json')
        self.assertIn(b'testuser1', response.data)
    

    def test_user_login_workS(self):
        response = self.app.post('/login', data=json.dumps(dict(
                username='testuser',
                password='testpass'
            )),
            content_type='application/json')
        self.assertIn(b'testuser', response.data)
