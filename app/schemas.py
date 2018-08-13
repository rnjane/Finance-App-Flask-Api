from marshmallow import Schema, fields, pprint


class UserSchema(Schema):
    username = fields.String()
    email = fields.String()


class BudgetSchema(Schema):
    name = fields.String()
    amount = fields.Float()


class MiniBudgetSchema(Schema):
    name = fields.String()
    amount = fields.Float()
