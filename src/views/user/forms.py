from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField,StringField, SelectField,IntegerField, DateField

from wtforms.validators import DataRequired

class BudgetForm(FlaskForm):
    budget_month = SelectField(
        "Select Month",
        validators=[DataRequired()],
        choices=[
            ('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'),
            ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'),
            ('09', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
        ])
    budget_year = IntegerField(validators=[DataRequired()])
    budget_amount = DecimalField("Budget Amount", validators=[DataRequired()])
    submit = SubmitField("Submit")


class ExpansesForm(FlaskForm):
    expanse_category = SelectField(validators=[DataRequired()], choices=[('1','Food'),('2','transport'),('3','Groceries'),('4','Shopping'),('5','Entertainment'),('6','Travel'),('7','Health'),('8','Bills')])
    expanse_amount = IntegerField(validators=[DataRequired()])
    expanse_desc = StringField("Short Description")
    expanse_date = DateField(validators=[DataRequired()])
    submit = SubmitField('Submit')