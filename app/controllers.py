import datetime
import os

from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
import jwt
from sqlalchemy import or_

from app import db, app
from app.models import User, Budget, MiniBudget
from app.schemas import UserSchema, BudgetSchema, MiniBudgetSchema


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
    def create_budget(self, user_id, budget_name, budget_amount):
        budget = Budget.query.filter_by(
            owner_id=user_id, name=budget_name).first()
        if budget:
            return "You are already using this budget name. Use a different" \
                " name"
        else:
            new_budget = Budget(
                owner_id=user_id, name=budget_name, amount=budget_amount)
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
            return BudgetSchema().dump(budget)
        else:
            return "There is no budget with this ID for you"

    def edit_budget(self, user_id, budget_id, new_name, new_amount):
        budget = Budget.query.filter_by(owner_id=user_id, id=budget_id).first()
        if budget:
            # NOTE: You forgot to make edits here
            db.session.commit()
            return MiniBudgetSchema().dump(budget)
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


class MiniBudgetController():
    def create_mini_budget(self, budget_id, mini_budget_name,
                           mini_budget_amount):
        mini_budget = MiniBudget.query.filter_by(
            budget_id=budget_id, name=mini_budget_name).first()
        if mini_budget:
            return "This name is already in use in this budget. Use a" \
                " different name"
        else:
            new_mini_budget = MiniBudget(
                budget_id=budget_id, name=mini_budget_name,
                amount=mini_budget_amount
            )
            db.session.add(new_mini_budget)
            db.session.commit()
            return MiniBudgetSchema().dump(new_mini_budget)

    def view_all_mini_budgets(self, budget_id):
        mini_budgets = MiniBudget.query.filter_by(budget_id=budget_id).all()
        if mini_budgets:
            return MiniBudgetSchema(many=True).dump(mini_budgets)
        else:
            return "You have no mini budgets in this budget"

    def view_one_mini_budget(self, budget_id, mini_budget_id):
        mini_budget = MiniBudget.query.filter_by(
            budget_id=budget_id, id=mini_budget_id).first()
        if mini_budget:
            return MiniBudgetSchema().dump(mini_budget)
        else:
            return "There is no mini budget with this ID in the " \
                "specified budget"

    def edit_mini_budget(self, budget_id, mini_budget_id, new_name=None,
                         new_amount=None):
        mini_budget = MiniBudget.query.filter_by(
            budget_id=budget_id, id=mini_budget_id).first()
        if mini_budget:
            # NOTE: No editing is performed here as well
            db.session.commit()
            return MiniBudgetSchema().dump(mini_budget)
        else:
            return "There is no mini budget with this ID in the specified" \
                " budget"

    def delete_mini_budget(self, budget_id, mini_budget_id):
        mini_budget = MiniBudget.query.filter_by(
            budget_id=budget_id, id=mini_budget_id).first()
        if mini_budget:
            db.session.delete(mini_budget)
            db.session.commit()
            return "Mini budget deleted Succesfully"
        else:
            return "There is no mini budget with this ID in the specified" \
                " budget"
