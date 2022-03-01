from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .process import get_and_clean_data
from .process import exampleoutput

main = Blueprint('main', __name__)
dataframe = get_and_clean_data()
dataexanple = exampleoutput(dataframe)

@main.route('/')
def index():
    return render_template('index.html', data=dataexanple)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
