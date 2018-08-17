from functools import wraps

from flask_restplus import Resource
from flask import request, jsonify
import jwt

from app import api, app
from app.controllers import UserController, BudgetController, ExpenseController, IncomeController, MiniExpenseController
from app.models import User
from app.schemas import UserSchema

user_object = UserController()
budget_object = BudgetController()
expense_object = ExpenseController()
income_object = IncomeController()
mini_expense_object = MiniExpenseController()


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
        if isinstance(response, User):
            return UserSchema().dump(response)
        else:
            print(response)
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

    """Create a budget"""
    def post(self, current_user):
        data = request.get_json()
        response = budget_object.create_budget(current_user.id, data['name'])
        if response == "You are already using this budget name. Use a different name":
            return response
        else:
            return response

    """view all budgets"""
    def get(self, current_user):
        response = budget_object.view_all_budgets(current_user.id)
        if response == "You have no budgets":
            return response
        else:
            return response


@api.route('/budgets/<budget_id>')
class Budget(Resource):
    decorators = [token_required]

    """view one budget"""
    def get(self, current_user, budget_id):
        response = budget_object.view_one_budget(
            user_id=current_user.id, budget_id=budget_id)
        if response == "You have no budgets":
            return response
        else:
            return response

    """edit a budget"""
    def put(self, current_user, budget_id):
        data = request.get_json()
        response = budget_object.edit_budget(user_id = current_user.id, budget_id = budget_id, new_name = data['newname'])
        if response == "There is no budget with this ID for you":
            return response
        else:
            return response

    """Delete a budget"""
    def delete(self, current_user, budget_id):
        response = budget_object.delete_budget(
            user_id=current_user.id, budget_id=budget_id)
        if response == "Budget deleted Succesfully":
            return response
        else:
            return response

@api.route('/<budget_id>/expenses/')
class Expenses(Resource):
    decorators = [token_required]

    """Create an expense"""
    def post(self, current_user, budget_id):
        data = request.get_json()
        response = expense_object.create_expense(budget_id = budget_id, expense_name = data['name'], amount = data['amount'])
        if response == "This name is already in use in this budget. Use a different name":
            return response
        else:
            return response

    """View all expenses"""
    def get(self, current_user, budget_id):
        response = expense_object.view_all_expenses(budget_id = budget_id)
        if response == "You have no expenses in this budget":
            return response
        else:
            return response

@api.route('/<budget_id>/expense/<expense_id>')
class Expense(Resource):
    decorators = [token_required]

    """Get one expense"""
    def get(self, current_user, budget_id, expense_id):
        response = expense_object.view_one_expense(budget_id = budget_id, expense_id = expense_id)
        if response == "There is no mini budget with this ID in the specified budget":
            return response
        else:
            return response

    """Edit an expense"""
    def put(self, current_user, budget_id, expense_id):
        data = request.get_json()
        response = expense_object.edit_expense(budget_id = budget_id, new_name = data['newname'], new_amount = data['newamount'], expense_id = expense_id)
        if response == "There is no expense with this ID in the specified budget":
            return response
        else:
            return response

    """Delete an expense"""
    def delete(self, user_id, budget_id, expense_id):
        response = expense_object.delete_expense(budget_id = budget_id, expense_id = expense_id)
        if response == "Expense deleted Succesfully":
            return response
        else:
            return response


@api.route('/<budget_id>/incomes/')
class Incomes(Resource):
    decorators = [token_required]

    """Create a new income endpoint"""
    def post(self, budget_id):
        data = request.get_json()
        response = income_object.create_income(budget_id = budget_id, income_name = data['name'], amount = data['amount'])
        if response == "This name is already in use in this budget. Use a different name":
            return response
        else:
            return response
    
    """Endpoint to get all incomes in a budget"""
    def get(self, current_user, budget_id):
        response = income_object.view_all_incomes(budget_id = budget_id)
        if response == "You have no incomes in this budget":
            return response
        else:
            return response

@api.route('/<budget_id>/income/<income_id>')
class Income(Resource):
    decorators = [token_required]

    """Endpoint to get one income in a budget by its ID"""
    def get(self, current_user, budget_id, income_id):
        response = income_object.view_one_income(budget_id = budget_id, income_id = income_id)
        if response == "There is no income with this ID in the specified budget":
            return response
        else:
            return response

    """Endpoint to edit an income in a budget"""
    def put(self, current_user, budget_id, income_id):
        data = request.get_json()
        response = income_object.edit_income(budget_id = budget_id, new_name = data['newname'], new_amount = data['newamount'], income_id = income_id)
        if response == "There is no income with this ID in the specified budget":
            return response
        else:
            return response

    """Endpoint to delete an income in a budget"""
    def delete(self, user_id, budget_id, income_id):
        response = income_object.delete_income(budget_id = budget_id, income_id = income_id)
        if response == "Income deleted Succesfully":
            return response
        else:
            return response


@api.route('/<expense_id>/mini-expenses/')
class MiniExpenses(Resource):
    decorators = [token_required]

    """Endpoint to create a new mini expense"""
    def post(self, expense_id):
        return "hello"
    
    """Endpoint to get all mini expenses in an expense"""
    def get(self, current_user, expense_id):
        response = mini_expense_object.view_all_mini_expenses(expense_id = expense_id)
        if response == "You have no mini expenses in this expense":
            return response
        else:
            return response

@api.route('/<expense_id>/income/<mini_expense_id>')
class Income(Resource):
    decorators = [token_required]

    """Endpoint to get one mini-expense in an expense by its ID"""
    def get(self, expense_id, mini_expense_id):
        response = mini_expense_object.view_one_mini_expense(expense_id = expense_id, mini_expense_id = mini_expense_id)
        if response == "There is no mini expense with this ID in the specified expense":
            return response
        else:
            return response

    """Endpoint to edit a mini-expense in an expense"""
    def put(self, current_user, expense_id, mini_expense_id):
        data = request.get_json()
        response = mini_expense_object.edit_mini_expense(expense_id = expense_id, new_name = data['newname'], new_amount = data['newamount'], mini_expense_id = mini_expense_id)
        if response == "There is no mini expense with this ID in the specified expense":
            return response
        else:
            return response

    """Endpoint to delete a mini-expense in an expense"""
    def delete(self, expense_id, mini_expense_id):
        response = mini_expense_object.delete_mini_expense(expense_id = expense_id, mini_expense_id = mini_expense_id)
        if response == "Mini Expense deleted Succesfully":
            return response
        else:
            return response
