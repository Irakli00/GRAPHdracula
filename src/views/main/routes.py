from flask import Blueprint, render_template

from src import User

main_blueprint = Blueprint('main', __name__, template_folder='templates')


@main_blueprint.route('/', methods=['GET']) 
def index():
    users = User.query.all()

    return render_template('main/index.html', users=users)
