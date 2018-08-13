from marshmallow import Schema, fields, pprint


class UserSchema(Schema):
    username = fields.String()
    email = fields.String()


class BudgetSchema(Schema):
    name = fields.String()
    total_income = fields.Float()
    total_expenses = fields.Float()


class ExpenseSchema(Schema):
    name = fields.String()
    amount = fields.Float()
    remaining_amount = fields.Float()

class IncomeSchema(Schema):
    name = fields.String()
    amount = fields.Float()

class MiniExpenseSchema(Schema):
    name = fields.String()
    amount = fields.Float()
