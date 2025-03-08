from flask import Blueprint, render_template, flash, redirect, url_for
from flask import jsonify, request
from flask_login import login_required, current_user
from datetime import datetime

from src.models import User, Budget, Expense
from src.extensions import db
from src.views.user.forms import BudgetForm, ExpansesForm

users_blueprint = Blueprint('user', __name__, template_folder='templates')


@users_blueprint.route('/user/<int:id>', methods=['GET','POST'])
@login_required
def user(id):
    budget_form = BudgetForm()
    expanses_form = ExpansesForm()
    user = User.query.get_or_404(id)

    if budget_form.validate_on_submit():
        budget_date = budget_form.budget_date.data
        budget_amount = budget_form.budget_amount.data

        month = budget_date[:2]
        users_every_budget = Budget.query.filter(Budget.user_id==user.id).all()

        for b in users_every_budget: #optimaze latter
            if b.month == month:
                b.amount = budget_amount
            else:
                new_budget_month = str(budget_form.budget_date.data[:2])
                new_budget_year = budget_form.budget_date.data[-4:]
                new_budget_amount = budget_form.budget_amount.data
                new_budget_user = current_user.id

                if not Budget.query.filter(Budget.month== new_budget_month, Budget.year== new_budget_year,Budget.user_id== new_budget_user).first():
                    new_budget = Budget(
                    amount=new_budget_amount,
                    year=new_budget_year,month=new_budget_month, user_id = new_budget_user
                    )

                    db.session.add(new_budget)
                    db.session.commit()

            db.session.commit()


    if expanses_form.validate_on_submit():
        expanse_category = expanses_form.expanse_category.data
        expanse_amount = expanses_form.expanse_amount.data
        expanse_desc = expanses_form.expanse_desc.data
        expanse_date = expanses_form.expanse_date.data

        new_expanse = Expense(amount = expanse_amount, description = expanse_desc, date = expanse_date, user_id = current_user.id, category_id = expanse_category)

        db.session.add(new_expanse)
        db.session.commit()

    if current_user.id != user.id:
        flash("You are not authorized to view this page.", "danger")
        return redirect(url_for('main.index'))
    
    user_budgets = Budget.query.filter(Budget.user_id == current_user.id)
    user_expanses = Expense.query.filter(Expense.user_id == current_user.id)
    
    return render_template('users/user.html', user=user, budget_form=budget_form, budgets = user_budgets, expanses_form = expanses_form, expanses = user_expanses)


@users_blueprint.route("/api/user/<int:id>/expenses")
def get_user_expenses(id):
    user = User.query.get_or_404(id)
    
    expenses_data = [
        {
            "amount": expense.amount,
            "description": expense.description,
            "date": expense.date.strftime("%d %B %Y"),
            "category":expense.category.name
        }
        for expense in user.expenses
    ]
    
    return jsonify(expenses_data)

