from functools import wraps

from flask_restplus import Resource
from flask import request, jsonify
import jwt

from app import api, app
from app.controllers import (
    UserController, BudgetController, MiniBudgetController
)
from app.models import User
from app.schemas import UserSchema

user_object = UserController()
budget_object = BudgetController()
mini_budget_object = MiniBudgetController()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('token')
        if not token:
            return jsonify({'message': 'Token is missing!'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(
                username=data['username']).first()
        except:
            return jsonify({'message': 'Token is invalid!'})
        return f(current_user, *args, **kwargs)

    return decorated


@api.route('/register')
class Register(Resource):
    def post(self):
        data = request.get_json()
        response = user_object.register(
            username=data['username'], email=data['email'],
            password1=data['password1'], password2=data['password2']
        )
        # NOTE: The edit here could work across all the endpoints
        # Just take not that it also involves editing the controllers a bit
        if isinstance(response, User):
            return UserSchema().dump(new_user)
        else:
            return response


@api.route('/login')
class Login(Resource):
    def post(self):
        data = request.get_json()
        response = user_object.login(
            username=data['username'], password=data['password'])
        if response == "Wrong password":
            return response
        elif response == "User with this username does not exist":
            return response
        else:
            return response


@api.route('/budgets')
class Budgets(Resource):
    decorators = [token_required]

    def post(self, current_user):
        data = request.get_json()
        response = budget_object.create_budget(
            current_user.id, data['name'], data['amount'])
        if response == "You are already using this budget name.' \
                ' Use a different name":
            return response
        else:
            return response

    def get(self, current_user):
        response = budget_object.view_all_budgets(current_user.id)
        if response == "You have no budgets":
            return response
        else:
            return response


@api.route('/budgets/<budget_id>')
class Budget(Resource):
    decorators = [token_required]

    def get(self, current_user, budget_id):
        response = budget_object.view_one_budget(
            user_id=current_user.id, budget_id=budget_id)
        if response == "You have no budgets":
            return response
        else:
            return response

    def put(self, current_user, budget_id):
        data = request.get_json()
        response = budget_object.edit_budget(
            user_id=current_user.id, budget_id=budget_id,
            new_name=data['newname'], new_amount=data['newamount']
        )
        if response == "There is no budget with this ID for you":
            return response
        else:
            return response

    def delete(self, current_user, budget_id):
        response = budget_object.delete_budget(
            user_id=current_user.id, budget_id=budget_id)
        if response == "Budget deleted Succesfully":
            return response
        else:
            return response


@api.route('/budgets/<budget_id>/mini-budget/')
class MiniBudgets(Resource):
    decorators = [token_required]

    def post(self, current_user, budget_id):
        data = request.get_json()
        response = mini_budget_object.create_mini_budget(
            budget_id=budget_id, mini_budget_name=data['name'],
            mini_budget_amount=data['amount']
        )
        if response == "This name is already in use in this budget.' \
                ' Use a different name":
            return response
        else:
            return response

    def get(self, current_user, budget_id):
        response = mini_budget_object.view_all_mini_budgets(
            budget_id=budget_id)
        if response == "You have no mini budgets in this budget":
            return response
        else:
            return response


@api.route('/budgets/<budget_id>/mini-budget/<mini_budget_id>')
class MiniBudget(Resource):
    decorators = [token_required]

    def get(self, current_user, budget_id, mini_budget_id):
        response = mini_budget_object.view_one_mini_budget(
            budget_id=budget_id, mini_budget_id=mini_budget_id)
        if response == "There is no mini budget with this ID in' \
                ' the specified budget":
            return response
        else:
            return response

    def put(self, current_user, budget_id, mini_budget_id):
        data = request.get_json()
        response = mini_budget_object.edit_mini_budget(
            budget_id=budget_id, new_name=data['newname'],
            new_amount=data['newamount'], mini_budget_id=mini_budget_id
        )
        if response == "There is no mini budget with this ID in the' \
                ' specified budget":
            return response
        else:
            return response

    def delete(self, user_id, budget_id, mini_budget_id):
        response = mini_budget_object.delete_mini_budget(
            budget_id=budget_id, mini_budget_id=mini_budget_id)
        if response == "Mini budget deleted Succesfully":
            return response
        else:
            return response
