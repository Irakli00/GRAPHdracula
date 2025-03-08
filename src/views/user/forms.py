from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField,StringField, SelectField,IntegerField, DateField

from wtforms.validators import DataRequired

class BudgetForm(FlaskForm):
    budget_date = StringField("Select Month", validators=[DataRequired()])
    budget_amount = DecimalField("Budget Amount", validators=[DataRequired()])
    submit = SubmitField("Submit")


class ExpansesForm(FlaskForm):
    expanse_category = SelectField(validators=[DataRequired()], choices=[('1','Food'),('2','transport'),('3','Groceries'),('4','Shopping'),('5','Entertainment'),('6','Travel'),('7','Health'),('8','Bills')])
    expanse_amount = IntegerField(validators=[DataRequired()])
    expanse_desc = StringField("Short Description")
    expanse_date = DateField(validators=[DataRequired()])
    submit = SubmitField('Submit')