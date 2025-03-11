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
        budget_month = budget_form.budget_month.data
        budget_year = budget_form.budget_year.data
        budget_amount = budget_form.budget_amount.data

        existiong_budget = Budget.query.filter(Budget.user_id==user.id, Budget.month == budget_month).first()
        print(current_user.id, existiong_budget)

        if existiong_budget:
            existiong_budget.amount = budget_amount
            db.session.commit() #changes db directly (bad)
        else:
            new_budget_month = str(budget_form.budget_date.data[:2])
            new_budget_year = budget_form.budget_date.data[-4:]
            new_budget_amount = budget_form.budget_amount.data
            new_budget_user = current_user.id

            new_budget = Budget(
                    amount=new_budget_amount,
                    year=new_budget_year,month=new_budget_month, user_id = new_budget_user
                    )
            db.session.add(new_budget)
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

    comperative = {
    '01': 0, '02': 1, '03': 2, '04': 3, '05': 4, '06': 5, '07': 6, '08': 7, '09': 8, '10': 9,
    '11': 10, '12': 11, '13': 12, '14': 13, '15': 14, '16': 15, '17': 16, '18': 17, '19': 18, '20': 19,
    '21': 20, '22': 21, '23': 22, '24': 23, '25': 24, '26': 25, '27': 26, '28': 27, '29': 28, '30': 29, '31': 30
    }
    
    expenses_data_ordered = []

    for ex in expenses_data:
        i = comperative[ex['date'][:2]]
        expenses_data_ordered.insert(i, ex)
    
    return jsonify(expenses_data_ordered)

