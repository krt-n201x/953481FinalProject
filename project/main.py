import pandas as pd
from flask import Blueprint, render_template, app, request
from flask_login import login_required, current_user
from . import dataexanple
from .models import Favorite
from .process import favoritesearchtfidf

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html', data=dataexanple)

@main.route('/home')
@login_required
def homeindex():
    return render_template('index.html', data=dataexanple, userid=current_user.id)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/favorite')
@login_required
def favorite():
    favorites = Favorite.query.filter(Favorite.userID == current_user.id).all()
    return render_template('favorite.html', data=favorites , userid=current_user.id)

@main.route('/favorite-search', methods=["POST"])
@login_required
def favoritesearch():
    tempJson = []
    inputword = request.form.get("inputword")
    # misobutter
    favorites = Favorite.query.filter(Favorite.userID == current_user.id).all()
    for i in favorites:
        tempJson.append([i.id,
                         i.foodTitle,
                         i.foodPicture])
    df = pd.DataFrame(tempJson, columns=["id", "foodTitle", "foodPicture"])
    data = favoritesearchtfidf(inputword,df)
    return render_template('favorite.html', data=data , userid=current_user.id)




