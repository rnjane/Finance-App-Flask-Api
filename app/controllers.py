import datetime
import os

from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
import jwt
from sqlalchemy import or_

from app import db, app
from app.models import User, Budget, Expense, Income, MiniExpense
from app.schemas import UserSchema, BudgetSchema, ExpenseSchema, MiniExpenseSchema, IncomeSchema


class UserController():
    def register(self, username, email, password1, password2):
        if password1 != password2:
            return "Passwords do not match"
        user = User.query.filter(
            or_(User.username == username, User.email == email)
        ).first()
        if user:
            return "Username and/or email in use. Use a different username" \
                " and/or email"
        password_hash = generate_password_hash(password1, method='sha256')
        new_user = User(username=username, email=email, password=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def login(self, username, password):
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                token = jwt.encode(
                    {'username': username,
                     "exp": datetime.datetime.utcnow() +
                     datetime.timedelta(minutes=3000)},
                    app.config['SECRET_KEY']
                )
                return jsonify({"token": token.decode('UTF-8'),
                                "username": user.username})
            else:
                return "Wrong password"
        else:
            return "User with this username does not exist"


class BudgetController():
    def create_budget(self, user_id, budget_name, total_income = 0, total_expenses = 0):
        budget = Budget.query.filter_by(owner_id = user_id, name = budget_name).first()
        if budget:
            return "You are already using this budget name. Use a different" \
                " name"
        else:
            new_budget = Budget(owner_id = user_id, name = budget_name, total_expenses = total_expenses, total_income = total_income)
            db.session.add(new_budget)
            db.session.commit()
            return BudgetSchema().dump(new_budget)

    def view_all_budgets(self, user_id):
        budgets = Budget.query.filter_by(owner_id=user_id).all()
        if budgets:
            return BudgetSchema(many=True).dump(budgets)
        else:
            return "You have no budgets"

    def view_one_budget(self, user_id, budget_id):
        budget = Budget.query.filter_by(owner_id=user_id, id=budget_id).first()
        if budget:
            response = {}
            response['name'] = budget.name
            response['Incomes'] = budget.total_income
            response['Expenses'] = budget.total_expenses
            return BudgetSchema().dump(response)
        else:
            return "There is no budget with this ID for you"

    def edit_budget(self, user_id, budget_id, new_name):
        budget = Budget.query.filter_by(owner_id = user_id, id = budget_id).first()
        if budget:
            budget.name = new_name
            db.session.commit()
            response = {}
            response['name'] = budget.name
            response['Incomes'] = budget.total_income
            response['Expenses'] = budget.total_expenses
            return BudgetSchema().dump(response)
        else:
            return "There is no budget with this ID for you"

    def delete_budget(self, user_id, budget_id):
        budget = Budget.query.filter_by(owner_id=user_id, id=budget_id).first()
        if budget:
            db.session.delete(budget)
            db.session.commit()
            return "Budget deleted Succesfully"
        else:
            return "There is no budget with this ID for you"

 
class ExpenseController():
    def create_expense(self, budget_id, expense_name, amount, remaining_amount = 0):
        expense = Expense.query.filter_by(budget_id = budget_id, name = expense_name).first()
        if expense:
            return "This name is already in use in this budget. Use a different name"
        else:
            new_expense = Expense(budget_id = budget_id, name = expense_name, amount = amount, remaining_amount = remaining_amount)
            db.session.add(new_expense)
            db.session.commit()
            response = {}
            response['name'] = new_expense.name
            response['budget id'] = new_expense.budget_id
            response['Total Amount'] = new_expense.amount
            response['Remaining Amount'] = new_expense.remaining_amount
            return ExpenseSchema().dump(response)

    def view_all_expenses(self, budget_id):
        expenses = Expense.query.filter_by(budget_id = budget_id).all()
        if expenses:
            expenses_list = []
            for expense in expenses:
                response = {}
                response['name'] = expense.name
                response['amount'] = expense.amount
                expenses_list.append(response)
            return ExpenseSchema().dump(expenses_list, many = True)
        else:
            return "You have no mini budgets in this budget"

    def view_one_expense(self, budget_id, expense_id):
        expense = Expense.query.filter_by(budget_id = budget_id, id = expense_id).first()
        if expense:
            response = {}
            response['name'] = expense.name
            response['amount'] = expense.amount
            response['remaining amout'] = expense.remaining_amount
            return ExpenseSchema().dump(response)
        else:
            return "There is no mini budget with this ID in the " \
                "specified budget"

    def edit_expense(self, budget_id, expense_id, new_name, new_amount):
        expense = Expense.query.filter_by(budget_id = budget_id, expense_id = expense_id).first()
        if expense:
            expense.name = new_name
            expense.amount = new_amount
            db.session.commit()
            response = {}
            response['name'] = expense.name
            response['amount'] = expense.amount
            return ExpenseSchema().dump(response)
        else:
            return "There is no expense with this ID in the specified budget"

    def delete_expense(self, budget_id, expense_id):
        expense = Expense.query.filter_by(budget_id = budget_id, expense_id = expense_id).first()
        if expense:
            db.session.delete(expense)
            db.session.commit()
            return "Expense deleted Succesfully"
        else:
            return "There is no expense with this ID in the specified budget"


class IncomeController():

    """Create a new income for a certain budget"""
    def create_income(self, budget_id, income_name, amount):
        income = Income.query.filter_by(budget_id = budget_id, name = income_name).first()
        if income:
            return "This name is already in use in this budget. Use a different name"
        else:
            new_income = Income(budget_id = budget_id, name = income_name, amount = amount)
            db.session.add(new_income)
            db.session.commit()
            response = {}
            response['name'] = new_income.name
            response['budget id'] = new_income.budget_id
            response['Total Amount'] = new_income.amount
            return IncomeSchema().dump(response)

    """View all incomes in a budget"""
    def view_all_incomes(self, budget_id):
        incomes = Income.query.filter_by(budget_id = budget_id).all()
        if incomes:
            income_list = []
            for income in incomes:
                response = {}
                response['name'] = income.name
                response['amount'] = income.amount
                income_list.append(response)
            return IncomeSchema().dump(income_list, many = True)
        else:
            return "You have no incomes in this budget"

    """View one income in a budget by ID"""
    def view_one_income(self, budget_id, income_id):
        income = Income.query.filter_by(budget_id = budget_id, id = income_id).first()
        if income:
            response = {}
            response['name'] = income.name
            response['amount'] = income.amount
            return IncomeSchema().dump(response)
        else:
            return "There is no income with this ID in the specified budget"

    """Update an income in a budget"""
    def edit_income(self, budget_id, income_id, new_name, new_amount):
        income = Income.query.filter_by(budget_id = budget_id, income_id = income_id).first()
        if income:
            income.name = new_name
            income.amount = new_amount
            db.session.commit()
            response = {}
            response['name'] = income.name
            response['amount'] = income.amount
            return IncomeSchema().dump(response)
        else:
            return "There is no income with this ID in the specified budget"

    """Delete an income in a budget"""
    def delete_income(self, budget_id, income_id):
        income = Income.query.filter_by(budget_id = budget_id, income_id = income_id).first()
        if income:
            db.session.delete(income)
            db.session.commit()
            return "Income deleted Succesfully"
        else:
            return "There is no income with this ID in the specified budget"


class MiniExpenseController():

    """Create a mini expense of an expense"""
    def create_mini_expense(self, expense_id, mini_expense_name, amount):
        mini_expense = Expense.query.filter_by(expense_id = expense_id, name = mini_expense_name).first()
        if mini_expense:
            return "This name is already in use in this expense. Use a different name"
        else:
            new_mini_expense = MiniExpense(expense_id = budget_id, name = expense_name, amount = amount)
            db.session.add(new_mini_expense)
            db.session.commit()
            response = {}
            response['name'] = new_mini_expense.name
            response['budget id'] = new_mini_expense.budget_id
            response['Total Amount'] = new_mini_expense.amount
            return MiniExpenseSchema().dump(response)

    """View all mini expenses in an expense"""
    def view_all_mini_expenses(self, expense_id):
        mini_expenses = MiniExpense.query.filter_by(expense_id = expense_id).all()
        if mini_expenses:
            mini_expenses_list = []
            for mini_expense in mini_expenses:
                response = {}
                response['name'] = mini_expense.name
                response['amount'] = mini_expense.amount
                mini_expenses_list.append(response)
            return MiniExpenseSchema().dump(mini_expenses_list, many = True)
        else:
            return "You have no mini expenses in this expense"

    """View a mini expense by its ID"""
    def view_one_mini_expense(self, expense_id, mini_expense_id):
        mini_expense = MiniExpense.query.filter_by(expense_id = expense_id, id = mini_expense_id).first()
        if mini_expense:
            response = {}
            response['name'] = mini_expense.name
            response['amount'] = mini_expense.amount
            return MiniExpenseSchema().dump(response)
        else:
            return "There is no mini expense with this ID in the specified expense"

    """Edit a mini_expense"""
    def edit_mini_expense(self, expense_id, mini_expense_id, new_name, new_amount):
        mini_expense = MiniExpense.query.filter_by(expense_id = expense_id, id = mini_expense_id).first()
        if mini_expense:
            mini_expense.name = new_name
            mini_expense.amount = new_amount
            db.session.commit()
            response = {}
            response['name'] = mini_expense.name
            response['amount'] = mini_expense.amount
            return MiniExpenseSchema().dump(response)
        else:
            return "There is no mini expense with this ID in the specified expense"

    """Delete a mini expense"""
    def delete_mini_expense(self, expense_id, mini_expense_id):
        mini_expense = MiniExpense.query.filter_by(expense_id = expense_id, id = mini_expense_id).first()
        if mini_expense:
            db.session.delete(mini_expense)
            db.session.commit()
            return "Mini Expense deleted Succesfully"
        else:
            return "There is no Mini expense with this ID in the specified expense"
