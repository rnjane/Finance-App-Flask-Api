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

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    amount = db.Column(db.Numeric, nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    # NOTE: Always a good idea to track the date something was modified
    date_modified = db.Column(db.DateTime, onupdate=datetime.utcnow)
    mini_budgets = db.relationship('MiniBudget', backref='budget', lazy=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return 'Budget Name:' % self.name


class MiniBudget(db.Model):
    __tablename__ = "mini_budget"

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
        return 'Mini Budget Name:' % self.name
