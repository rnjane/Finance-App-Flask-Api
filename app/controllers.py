from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, json
import simplejson
import datetime
import jwt


from app import db, app
from app.models import User, Budget, MiniBudget


class UserController():
    def register(self, username, email, password1, password2):
        if password1 != password2:
            return "Passwords do not match"
        user = User.query.filter_by(username = username).first()
        if user:
            return "Username and/or email in use. Use a differnet username and/or email"
        password_hash = generate_password_hash(password1, method='sha256')
        new_user = User(username = username, email = email, password = password_hash)
        db.session.add(new_user)
        db.session.commit()
        return User.query.filter_by(username = username, email = email).first().username

    def login(self, username, password):
        user = User.query.filter_by(username = username).first()
        if user:
            if check_password_hash(user.password, password):
                token = jwt.encode({'username': username, "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes=3000)}, app.config['SECRET_KEY'])
                return jsonify({"token" : token.decode('UTF-8'), "username" : user.username})
            else:
                return "Wrong password"
        else:
            return "User with this username does not exist"


class BudgetController():
    def create_budget(self, user_id, budget_name, budget_amount):
        budget = Budget.query.filter_by(owner_id = user_id, name = budget_name).first()
        if budget:
            return "You are already using this budget name. Use a different name"
        else:
            new_budget = Budget(owner_id = user_id, name = budget_name, amount = budget_amount)
            db.session.add(new_budget)
            db.session.commit()
            response = {}
            response['name'] = new_budget.name
            response['amount'] = new_budget.amount
            return json.dumps({'New Budget': response})

    def view_all_budgets(self, user_id):
        budgets = Budget.query.filter_by(owner_id = user_id).all()
        if budgets:
            output = []
            response = {}
            for budget in budgets:
                response['name'] = budget.name
                response['amount'] = budget.amount
                output.append(response)
            return json.dumps({'Budget' : output})
        else:
            return "You have no budgets"

    def view_one_budget(self, user_id, budget_id):
        budget = Budget.query.filter_by(owner_id = user_id, id = budget_id).first()
        if budget:
            response = {}
            response['name'] = budget.name
            response['amount'] = budget.amount
            return json.dumps({'Budget' : response})
        else:
            return "There is no budget with this ID for you"

    def edit_budget(self, user_id, budget_id, new_name, new_amount):
        budget = Budget.query.filter_by(owner_id = user_id, id = budget_id).first()
        if budget:
            if new_name:
                budget.name = new_name
            if new_amount:
                budget.amount = new_amount
            db.session.commit()
            response = {}
            response['name'] = budget.name
            response['amount'] = budget.amount
            return json.dumps({"Budget": response})
        else:
            return "There is no budget with this ID for you"


    def delete_budget(self, user_id, budget_id):
        budget = Budget.query.filter_by(owner_id = user_id, id = budget_id).first()
        if budget:
            db.session.delete(budget)
            db.session.commit()
            return "Budget deleted Succesfully"
        else:
            return "There is no budget with this ID for you"

 
class MiniBudgetController():
    def create_mini_budget(self, budget_id, mini_budget_name, mini_budget_amount):
        mini_budget = MiniBudget.query.filter_by(budget_id = budget_id, name = mini_budget_name).first()
        if mini_budget:
            return "This name is already in use in this budget. Use a different name"
        else:
            new_mini_budget = MiniBudget(budget_id = budget_id, name = mini_budget_name, amount = mini_budget_amount)
            db.session.add(new_mini_budget)
            db.session.commit()
            response = {}
            response['name'] = new_mini_budget.name
            response['amount'] = new_mini_budget.amount
            return json.dumps({"budget": response})

    def view_all_mini_budgets(self, budget_id):
        mini_budgets = MiniBudget.query.filter_by(budget_id = budget_id).all()
        if mini_budgets:
            response = {}
            mb_list = []
            for mini_budget in mini_budgets:
                response['name'] = mini_budget.name
                response['amount'] = mini_budget.amount
                mb_list.append(response)
            return json.dumps({"Mini Budgets": mb_list})
        else:
            return "You have no mini budgets in this budget"

    def view_one_mini_budget(self, budget_id, mini_budget_id):
        mini_budget = MiniBudget.query.filter_by(budget_id = budget_id, id = mini_budget_id).first()
        if mini_budget:
            response = {}
            response['name'] = mini_budget.name
            response['amount'] = mini_budget.amount
            return json.dumps({"mini budget": response})
        else:
            return "There is no mini budget with this ID in the specified budget"

    def edit_mini_budget(self, budget_id, mini_budget_id, new_name, new_amount):
        mini_budget = MiniBudget.query.filter_by(budget_id = budget_id, id = mini_budget_id).first()
        if mini_budget:
            if new_name:
                mini_budget.name = new_name
            if new_amount:
                mini_budget.amount = new_amount
            db.session.commit()
            response = {}
            response['name'] = mini_budget.name
            response['amount'] = mini_budget.amount
            return json.dumps({"Mini budget": response})
        else:
            return "There is no mini budget with this ID in the specified budget"

    def delete_mini_budget(self, budget_id, mini_budget_id):
        mini_budget = MiniBudget.query.filter_by(budget_id = budget_id, id = mini_budget_id).first()
        if mini_budget:
            db.session.delete(mini_budget)
            db.session.commit()
            return "Mini budget deleted Succesfully"
        else:
            return "There is no mini budget with this ID in the specified budget"