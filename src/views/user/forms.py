from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField,StringField

from wtforms.validators import DataRequired

class BudgetForm(FlaskForm):
    budget_date = StringField("Select Month", validators=[DataRequired()])
    budget_amount = DecimalField("Budget Amount", validators=[DataRequired()])
    submit = SubmitField("Submit")
