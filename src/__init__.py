from flask import Flask
from flask_admin.contrib.sqla import ModelView

from src.config import Config
from src.extensions import db, login_manager, migrate
# from src.admin import admin, BookView,  AuthorView, SeriesView, ThemeView, PublisherView, CollectionView, PublishLocationView
from src.commands import init_db_command, populate_db_command
from src.models import User
from src.views import users_blueprint, main_blueprint, auth_blueprint

COMMANDS = [
    init_db_command,
    populate_db_command
]

BLUEPRINTS = [
    users_blueprint,
    main_blueprint,
    auth_blueprint
]


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extenstions(app)
    register_commands(app)
    register_blueprints(app)
    

    return app

def register_extenstions(app):
    db.init_app(app)

    migrate.init_app(app, db)

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    #
    # admin.init_app(app)
    #
    # admin.add_view(BookView(Book, db.session, name = "წიგნები"))
    #
    # admin.add_view(AuthorView(Author, db.session, category = "წიგნის მახასიათებლები", name = "რედაქტორები"))
    # admin.add_view(SeriesView(Series, db.session, category = "წიგნის მახასიათებლები", name = "სერიები"))
    # admin.add_view(PublisherView(Publisher, db.session,  category = "წიგნის მახასიათებლები", name = "გამომცემლობის სახელები"))
    # admin.add_view(ThemeView(Theme, db.session, category = "წიგნის მახასიათებლები", name =  "თემატიკები"))
    # admin.add_view(CollectionView(Collection, db.session, category = "წიგნის მახასიათებლები", name =  "კოლექციები"))
    # admin.add_view(PublishLocationView(PublishLocation, db.session, category =  "წიგნის მახასიათებლები", name = "გამოცემის ადგილები"))


def register_blueprints(app):
    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)   



def register_commands(app):
    for command in COMMANDS:
        app.cli.add_command(command)