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
            "date": expense.date.strftime("%Y-%m"),
            "category":expense.category.name
        }
        for expense in user.expenses
    ]
    
    return jsonify(expenses_data)

@users_blueprint.route("/api/user/budget",methods=['POST','GET'])
def budget():
    data = request.get_json()

    date = data.get('budget_date').split('-')
    print(data)
    
    budget_month = date[0]
    budget_year = date[1]
    budget_amount = data.get('budget_amount')
    
    try:
        new_budget = Budget(
            amount=float(budget_amount),
            year=budget_year,month=budget_month, user_id = current_user.id
        )
        db.session.add(new_budget)
        db.session.commit()

        return jsonify({
                "success": True,
                "message": "Budget created successfully!",
                "budget": {
                    "id": new_budget.id,
                    "month": new_budget.month,
                    "year":new_budget.year,
                    "amount": new_budget.amount
                }
            }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Error creating budget: {str(e)}"}), 500

@users_blueprint.route("/api/user/expanses", methods=["POST","GET"])
def expanse():
    data = request.get_json().get('formData')
    print(data)

    exp_category = data.get('category')
    exp_amount = data.get('expanse_amount')
    exp_desc= data.get('description')
    exp_date_str = data.get('expanse_date')

    exp_date = datetime.strptime(exp_date_str, "%Y-%m-%d").date()

    print(exp_amount,exp_category,exp_date,exp_desc)
    
    try:
        new_expanse= Expense(category_id=exp_category,amount=exp_amount, description=exp_desc, date=exp_date, user_id= current_user.id)

        db.session.add(new_expanse)
        db.session.commit()

        return jsonify({
                "success": True,
                "message": "expanse created successfully!",
                "expanse": {
                    "amount": new_expanse.amount,
                    "description":new_expanse.description,
                    "date": new_expanse.date,
                    "category":new_expanse.category_id
                }
            }), 201
    
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"success": False, "message": f"Error creating expanse: {str(e)}"}), 500