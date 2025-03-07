from datetime import datetime
from flask.cli import with_appcontext
import click

from src.models import User, Expense, Budget, Category
from src.extensions import db

def init_db():
    db.drop_all()
    db.create_all()

@click.command("init_db")
@with_appcontext
def init_db_command():
    click.echo("Database creation in porgress")
    init_db()
    click.echo("Database created")



@click.command("populate_db")
@with_appcontext
def populate_db_command():
    click.echo("populating db")

    category_food = Category(name="Food")
    category_transport = Category(name="Transport")
    category_groceries = Category(name="Groceries")
    category_shopping = Category(name="Shopping")
    category_entertainment = Category(name="Entertainment")
    category_travel = Category(name="Travel")
    category_health = Category(name="Health")
    category_bills = Category(name="Bills")

    db.session.add_all([category_food, category_transport, category_groceries,  category_shopping,category_entertainment, category_travel, category_health, category_bills])
    db.session.commit()

    user1 = User(username="willy_bonkya", email="willy_bonkya@chocolatefactory.com", password="willy_bonka123",profile_photo = 'random.png')
    user1.password = 'willy_bonka123'
    user2 = User(username="bobby_brasko", email="notacop@forshure.com", password="password", profile_photo = 'Untitled.jpeg')
    user2.password = 'password'

    db.session.add_all([user1, user2])  #make those .create() from baseModel latter
    db.session.commit() #to get id-s

 
    expense1 = Expense(amount=50.00, description="had a lunch", date=datetime(2025, 3, 1), user_id=user1.id, category_id=category_food.id)
    expense2 = Expense(amount=120.00, description="had a lunch", date=datetime(2025, 3, 2), user_id=user1.id, category_id=category_food.id)
    expense3 = Expense(amount=75.50, description="took a train", date=datetime(2025, 3, 3), user_id=user2.id, category_id=category_transport.id)
    expense4 = Expense(amount=85.00, description="had dinner", date=datetime(2025, 3, 4), user_id=user1.id, category_id=category_food.id)
    expense5 = Expense(amount=30.00, description="coffee break", date=datetime(2025, 3, 5), user_id=user1.id, category_id=category_food.id)
    expense6 = Expense(amount=150.00, description="groceries", date=datetime(2025, 3, 6), user_id=user1.id, category_id=category_groceries.id)
    expense7 = Expense(amount=45.00, description="pizza night", date=datetime(2025, 3, 7), user_id=user1.id, category_id=category_food.id)
    expense8 = Expense(amount=60.00, description="brunch", date=datetime(2025, 3, 8), user_id=user1.id, category_id=category_food.id)

    # For user2
    expense9 = Expense(amount=80.00, description="bus ticket", date=datetime(2025, 3, 4), user_id=user2.id, category_id=category_transport.id)
    expense10 = Expense(amount=100.00, description="taxi ride", date=datetime(2025, 3, 5), user_id=user2.id, category_id=category_transport.id)
    expense11 = Expense(amount=200.00, description="monthly metro pass", date=datetime(2025, 3, 6), user_id=user2.id, category_id=category_transport.id)
    expense12 = Expense(amount=40.00, description="bike rental", date=datetime(2025, 3, 7), user_id=user2.id, category_id=category_transport.id)
    expense13 = Expense(amount=30.00, description="train ride", date=datetime(2025, 3, 8), user_id=user2.id, category_id=category_transport.id)

    # New categories for user1 and user2
    expense14 = Expense(amount=150.00, description="shopping spree", date=datetime(2025, 3, 5), user_id=user1.id, category_id=category_shopping.id)
    expense15 = Expense(amount=95.00, description="groceries shopping", date=datetime(2025, 3, 6), user_id=user2.id, category_id=category_groceries.id)
    expense16 = Expense(amount=200.00, description="weekend trip", date=datetime(2025, 3, 9), user_id=user1.id, category_id=category_travel.id)
    expense17 = Expense(amount=80.00, description="movie night", date=datetime(2025, 3, 10), user_id=user2.id, category_id=category_entertainment.id)
    expense18 = Expense(amount=50.00, description="gym membership", date=datetime(2025, 3, 12), user_id=user1.id, category_id=category_health.id)
    expense19 = Expense(amount=120.00, description="electricity bill", date=datetime(2025, 3, 13), user_id=user2.id, category_id=category_bills.id)

    # Add all expenses to the session
    db.session.add_all([expense1, expense2, expense3, expense4, expense5, expense6, expense7, expense8, 
                        expense9, expense10, expense11, expense12, expense13, expense14, expense15, 
                        expense16, expense17, expense18, expense19])


    budget1 = Budget( amount=5000.00, month='03', year=2025, user_id=user1.id)
    budget3 = Budget( amount=2000.00, month='03', year=2025, user_id=user2.id)

    db.session.add_all([budget1, budget3])

    db.session.commit()
