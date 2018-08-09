from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    date_modified = db.Column(db.DateTime, onupdate=datetime.utcnow)
    budgets = db.relationship('Budget', backref='user', lazy=True)
    # QUESTION: Why do you prefer lazy=True?

    def __repr__(self):
        return 'Username %r' % (self.username)


class Budget(db.Model):
    __tablename__ = "budget"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40), nullable = False)
    total_income = db.Column(db.Numeric, nullable = False)
    total_expenses = db.Column(db.Numeric, nullable = False)
    date_created = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    date_modified = db.Column(db.DateTime, onupdate=datetime.utcnow)
    expenses = db.relationship('Expense', backref='budget', lazy=True)
    income = db.relationship('Income', backref='budget', lazy=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return 'Budget Name %r' % (self.name)

class Expense(db.Model):
    __tablename__ = "expense"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40), nullable = False)
    amount = db.Column(db.Numeric, nullable = False)
    remaining_amount = db.Column(db.Numeric, nullable = False)
    date_created = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.id'), nullable = False)
    mini_expenses = db.relationship('MiniExpense', backref='expense', lazy=True)

    def __repr__(self):
        return 'Expense Name: %r' % (self.name)


class MiniExpense(db.Model):
    __tablename__ = "mini-expense"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40), nullable = False)
    amount = db.Column(db.Numeric, nullable = False)
    date_created = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    expense_id = db.Column(db.Integer, db.ForeignKey('expense.id'), nullable = False)

    def __repr__(self):
        return 'Mini-Expense Name: %r' % (self.name)


class Income(db.Model):
    __tablename__ = "income"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    amount = db.Column(db.Numeric, nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    date_modified = db.Column(db.DateTime, onupdate=datetime.utcnow)
    budget_id = db.Column(db.Integer, db.ForeignKey(
        'budget.id'), nullable=False)

    def __repr__(self):
        return 'Income Name: %r' % (self.name)
