from tests import FinanceAppTestSetup
import json

class BudgetsTests(FinanceAppTestSetup):
    """budgets functionalities tests"""
    
    def test_create_budget_succesful(self):
        token = self.app.post('/login', data=json.dumps(dict(
            username='testuser',
            password='testpass'
        )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        response = self.app.post('/budgets', headers=dict(
                                token=[tkn]), data=json.dumps(dict(
                                    name='newbudget'
                                )),
                                content_type='application/json')
        self.assertIn(b'newbudget', response.data)

    def test_view_one_budget_succesful(self):
        token = self.app.post('/login', data=json.dumps(dict(
            username='testuser',
            password='testpass'
        )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']
        response = self.app.get('/budgets/1', headers=dict(
            token=[tkn]))

        self.assertIn(b"testbudget", response.data)

    def test_view_all_budgets_succesful(self):
        token = self.app.post('/login', data=json.dumps(dict(
            username='testuser',
            password='testpass'
        )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        testview = self.app.get('/budgets', headers=dict(
                                token=[tkn]))

        self.assertIn(b"testbudget", testview.data)

    def test_edit_budget_succesful(self):
        token = self.app.post('/login', data=json.dumps(dict(
            username='testuser',
            password='testpass'
        )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        response = self.app.put('/budgets/1', headers=dict(
                                token=[tkn]), data=json.dumps(dict(
                                    newname='dojo'
                                )),
                                content_type='application/json')

        self.assertIn(b'dojo', response.data)


    def test_delete_budget_succesful(self):
        token = self.app.post('/login', data=json.dumps(dict(
            username='testuser',
            password='testpass'
        )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        response = self.app.delete('/budgets/2', headers=dict(
            token=[tkn]))
        self.assertIn(b'Budget deleted Succesfully', response.data)
