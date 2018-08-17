from tests import FinanceAppTestSetup
import json

class ExpensesTests(FinanceAppTestSetup):
    def test_add_expense_succesful(self):
        '''test adding an expense works'''
        token = self.app.post('/login', data=json.dumps(dict(
                username='testuser',
                password='testpass'
            )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        response = self.app.post("1/expenses/", headers=dict(
                                token=[tkn]), data=json.dumps(dict(
                name='testexpense',
                amount=20000
            )),
            content_type='application/json')

        self.assertIn(b"testexpense", response.data)

    def test_view_one_expense(self):
        '''test viewing one expense work'''
        token = self.app.post('/login', data=json.dumps(dict(
                username='testuser',
                password='testpass'
            )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        response = self.app.get("1/expense/1", headers=dict(
                                token=[tkn]))
        self.assertIn(b"testexpense1", response.data)

    def test_view_all_expenses_succes(self):
        '''test viewing all expenses work'''
        token = self.app.post('/login', data=json.dumps(dict(
                username='testuser',
                password='testpass'
            )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        response = self.app.get("1/expenses/", headers=dict(
                                token=[tkn]))
        self.assertIn(b"testexpense1", response.data)

    def test_expense_edit_succes(self):
        '''test expense edit works'''
        token = self.app.post('/login', data=json.dumps(dict(
                username='testuser',
                password='testpass'
            )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        response = self.app.put('1/expense/1', headers=dict(
                                token=[tkn]), data=json.dumps(dict(
                newname='andela',
                newamount=50000
            )),
            content_type='application/json')
        self.assertIn(b'andela', response.data)

    def test_expense_delete_succesful(self):
        '''test expense delete works'''
        token = self.app.post('/login', data=json.dumps(dict(
                username='testuser',
                password='testpass'
            )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        response = self.app.delete('1/expense/1', headers=dict(
                                token=[tkn]))
        self.assertIn(b'Expense deleted Succesfully', response.data)


class MiniExpense(FinanceAppTestSetup):
    def test_add_mini_expense_succesful(self):
        '''test adding a mini-expense works'''
        token = self.app.post('/login', data=json.dumps(dict(
                username='testuser',
                password='testpass'
            )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        response = self.app.post("2/mini-expenses", headers=dict(
                                token=[tkn]), data=json.dumps(dict(
                name='test mini expense',
                amount=30000
            )),
            content_type='application/json')

        self.assertIn(b"test mini expense", response.data)

#     def test_view_one_item_succes(self):
#         '''test viewing all items work'''
#         token = self.app.post('/auth/login', data=json.dumps(dict(
#                 username='testuser',
#                 password='testpass'
#             )),
#             content_type='application/json')

#         data = json.loads(token.data.decode())
#         tkn = data['token']

#         response = self.app.get("/bucketlists/2/items/1", headers=dict(
#                                 token=[tkn]))
#         self.assertIn(b"itemname", response.data)

#     def test_view_all_item_succes(self):
#         '''test viewing all items work'''
#         token = self.app.post('/auth/login', data=json.dumps(dict(
#                 username='testuser',
#                 password='testpass'
#             )),
#             content_type='application/json')

#         data = json.loads(token.data.decode())
#         tkn = data['token']

#         response = self.app.get("/bucketlists/2/items", headers=dict(
#                                 token=[tkn]))
#         self.assertIn(b"itemname", response.data)

#     def test_itemedit_succes(self):
#         '''test item edit works'''
#         token = self.app.post('/auth/login', data=json.dumps(dict(
#                 username='testuser',
#                 password='testpass'
#             )),
#             content_type='application/json')

#         data = json.loads(token.data.decode())
#         tkn = data['token']

#         response = self.app.put('/bucketlists/2/items/1', headers=dict(
#                                 token=[tkn]), data=json.dumps(dict(
#                 newname='andela',
#                 status='Done'
#             )),
#             content_type='application/json')
#         self.assertIn(b'Item has been updated!', response.data)

#     def test_itemdelete_succes(self):
#         '''test item delete works'''
#         token = self.app.post('/auth/login', data=json.dumps(dict(
#                 username='testuser',
#                 password='testpass'
#             )),
#             content_type='application/json')

#         data = json.loads(token.data.decode())
#         tkn = data['token']

#         response = self.app.delete('/bucketlists/2/items/1', headers=dict(
#                                 token=[tkn]))
#         self.assertIn(b'Item deleted!', response.data)