from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from src.extensions import db

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    profile_photo = db.Column(db.String, nullable=True)

    # password_hash = db.Column(db.String(255), nullable=False)
    _password = db.Column(db.String(255), nullable=False)

    expenses = db.relationship('Expense', backref='user', lazy=True)
    budget = db.relationship('Budget', backref='user', lazy=True, uselist=False)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f"<User {self.username}>"
