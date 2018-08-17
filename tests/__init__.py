import unittest
from app import app, config, db
from app.models import User, Budget, Expense
from werkzeug.security import generate_password_hash

class FinanceAppTestSetup(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config.from_object(config.TestingConfig)
        db.create_all()
        db.session.add(User(username='testuser', email='testuser@testuser.com', password=generate_password_hash(
            'testpass', method='sha256')))
        db.session.add(Budget(name='testbudget', total_income=0, total_expenses=0, owner_id=1))
        db.session.add(Budget(name='testbudget2', total_income=0, total_expenses=0, owner_id=1))
        db.session.add(Expense(name='testexpense1', amount=10000, budget_id=1, remaining_amount=0))
        db.session.add(Expense(name='testexpense2', amount=10000, budget_id=1, remaining_amount=0))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == "__main__":
    unittest.main()
