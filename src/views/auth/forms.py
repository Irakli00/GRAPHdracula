from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email,Length,EqualTo
from flask_wtf.file import FileField, FileAllowed



class LogInForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    profile_pic = FileField('Profile Picture',validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')