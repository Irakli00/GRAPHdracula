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
    user2 = User(username="bobby_brasko", email="notacop@forsure.com", password="password", profile_photo = 'Untitled.jpeg')
    user2.password = 'password'

    db.session.add_all([user1, user2])  #make those .create() from baseModel latter
    db.session.commit() #to get id-s

 


    # Expenses for User 1
    expense1 = Expense(amount=50.00, description="Gourmet sushi platter", date=datetime(2025, 3, 1), user_id=user1.id, category_id=category_food.id)
    expense2 = Expense(amount=120.00, description="Luxury wine tasting", date=datetime(2025, 3, 2), user_id=user1.id, category_id=category_food.id)
    expense3 = Expense(amount=75.50, description="Helicopter tour ticket", date=datetime(2025, 3, 3), user_id=user2.id, category_id=category_transport.id)
    expense4 = Expense(amount=85.00, description="Imported cheese selection", date=datetime(2025, 3, 4), user_id=user1.id, category_id=category_food.id)
    expense5 = Expense(amount=30.00, description="Molecular gastronomy snack", date=datetime(2025, 3, 5), user_id=user1.id, category_id=category_food.id)
    expense6 = Expense(amount=150.00, description="Ancient artifact auction", date=datetime(2025, 3, 6), user_id=user1.id, category_id=category_groceries.id)
    expense7 = Expense(amount=45.00, description="Handmade chocolate sculpture", date=datetime(2025, 3, 7), user_id=user1.id, category_id=category_food.id)
    expense8 = Expense(amount=60.00, description="Alien-themed ice cream", date=datetime(2025, 3, 8), user_id=user1.id, category_id=category_food.id)
    expense9 = Expense(amount=150.00, description="Cyberpunk fashion set", date=datetime(2025, 3, 5), user_id=user1.id, category_id=category_shopping.id)
    expense10 = Expense(amount=200.00, description="Zero-gravity flight experience", date=datetime(2025, 3, 9), user_id=user1.id, category_id=category_travel.id)
    expense11 = Expense(amount=50.00, description="Crystal energy healing session", date=datetime(2025, 3, 12), user_id=user1.id, category_id=category_health.id)

    # Expenses for User 2
    expense12 = Expense(amount=80.00, description="Vintage steam train ride", date=datetime(2025, 3, 4), user_id=user2.id, category_id=category_transport.id)
    expense13 = Expense(amount=100.00, description="Self-driving car rental", date=datetime(2025, 3, 5), user_id=user2.id, category_id=category_transport.id)
    expense14 = Expense(amount=200.00, description="Submarine adventure pass", date=datetime(2025, 3, 6), user_id=user2.id, category_id=category_transport.id)
    expense15 = Expense(amount=40.00, description="Space-themed scooter ride", date=datetime(2025, 3, 7), user_id=user2.id, category_id=category_transport.id)
    expense16 = Expense(amount=95.00, description="Golden fruit purchase", date=datetime(2025, 3, 6), user_id=user2.id, category_id=category_groceries.id)
    expense17 = Expense(amount=120.00, description="Time traveler’s insurance", date=datetime(2025, 3, 13), user_id=user2.id, category_id=category_bills.id)
    expense18 = Expense(amount=30.00, description="Teleportation hub fee", date=datetime(2025, 3, 8), user_id=user2.id, category_id=category_transport.id)
    expense19 = Expense(amount=80.00, description="VIP holographic concert", date=datetime(2025, 3, 10), user_id=user2.id, category_id=category_entertainment.id)

    # New Expenses for User 1 (with existing categories)
    expense20 = Expense(amount=70.00, description="Brunch with coworkers", date=datetime(2025, 3, 15), user_id=user1.id, category_id=category_food.id)
    expense21 = Expense(amount=55.00, description="Weekend city tour", date=datetime(2025, 3, 16), user_id=user1.id, category_id=category_travel.id)
    expense22 = Expense(amount=120.00, description="New shoes for work", date=datetime(2025, 3, 17), user_id=user1.id, category_id=category_shopping.id)
    expense23 = Expense(amount=40.00, description="Utility bill (internet)", date=datetime(2025, 3, 18), user_id=user1.id, category_id=category_bills.id)
    expense24 = Expense(amount=25.00, description="Fitness class pass", date=datetime(2025, 3, 19), user_id=user1.id, category_id=category_health.id)

    # New Expenses for User 2 (with existing categories)
    expense25 = Expense(amount=50.00, description="Art supplies for project", date=datetime(2025, 3, 20), user_id=user2.id, category_id=category_shopping.id)
    expense26 = Expense(amount=180.00, description="Luxury spa day", date=datetime(2025, 3, 21), user_id=user2.id, category_id=category_health.id)
    expense27 = Expense(amount=40.00, description="Taxi to airport", date=datetime(2025, 3, 22), user_id=user2.id, category_id=category_transport.id)
    expense28 = Expense(amount=60.00, description="Groceries for the weekend", date=datetime(2025, 3, 23), user_id=user2.id, category_id=category_groceries.id)
    expense29 = Expense(amount=30.00, description="Fast food delivery", date=datetime(2025, 3, 24), user_id=user2.id, category_id=category_food.id)
    expense30 = Expense(amount=100.00, description="Streaming service subscription", date=datetime(2025, 3, 25), user_id=user2.id, category_id=category_entertainment.id)


    db.session.add_all([
        expense1, expense2, expense3, expense4, expense5, expense6, expense7, expense8, 
        expense9, expense10, expense11, expense12, expense13, expense14, expense15, 
        expense16, expense17, expense18, expense19, 
        expense20, expense21, expense22, expense23, expense24, 
        expense25, expense26, expense27, expense28, expense29, expense30
    ])


    budget1 = Budget( amount=5000.00, month='03', year=2025, user_id=user1.id)
    budget3 = Budget( amount=2000.00, month='03', year=2025, user_id=user2.id)

    db.session.add_all([budget1, budget3])

    db.session.commit()
