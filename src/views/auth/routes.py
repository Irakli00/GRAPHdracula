from flask import render_template, url_for, redirect ,flash,  Blueprint
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import os
import uuid

from src.views.auth.forms import LogInForm, SignUpForm
from src.models import User
from src.extensions import db
from src.config import Config


auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login/', methods=['GET', 'POST'])
def logIn():
    form = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
        else:
            return render_template('auth/logIn.html', form=form, error='Invalid username or password')

        flash("You have been logged in.", "success")
        return redirect(url_for('user.user', id=user.id))
    
    return render_template('auth/logIn.html', form=form)

@auth_blueprint.route('/signUp', methods =['POST','GET'])
def signUp():
    logout_user()

    def generate_uuid_filename(filename):
        unique_filename = str(uuid.uuid4().hex[:18]) 
        _, file_extension = os.path.splitext(filename)
        return f"{unique_filename}{file_extension}"

    form = SignUpForm()

    if form.validate_on_submit():
        filename = None
        
        if form.profile_pic.data:
            file = form.profile_pic.data
            filename = generate_uuid_filename(file.filename)
            file.save(os.path.join(Config.UPLOAD_PATH, filename))

        email_exists = User.query.filter_by(email=form.email.data).first()
        if email_exists:
            flash("Email already registered", "danger")
            return redirect(url_for('auth.signUp'))
        
        hashed_password = generate_password_hash(form.password.data)
        
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, profile_photo = filename)

        db.session.add(new_user)
        db.session.commit() #make into .create()

        flash("Account created successfully!", "success")
        login_user(new_user)

        return redirect(url_for('user.user', id=new_user.id))  

    return render_template('auth/signUp.html', form=form)

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.logIn'))
