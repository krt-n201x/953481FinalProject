import pandas as pd
from flask import Blueprint, render_template, app, request
from flask_login import login_required, current_user
from . import dataexample, dataframe
from .models import Favorite
from .process import favoritesearchtfidf, wordsuggestion,findfooddetails

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html', data=dataexample)

@main.route('/home')
@login_required
def homeindex():
    return render_template('index.html', data=dataexample, userid=current_user.id)

@main.route('/readindetails', methods=['POST'])
@login_required
def fooddetails():
    fooddetails = request.form.get("foodTitle")
    data = findfooddetails(dataframe,fooddetails)
    return render_template('fooddetails.html', data=data)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/favorite')
@login_required
def favorite():
    favorites = Favorite.query.filter(Favorite.userID == current_user.id).all()
    suggestwordreturn = ""
    return render_template('favorite.html', data=favorites , userid=current_user.id,suggestword=suggestwordreturn)

@main.route('/favorite-search', methods=["POST"])
@login_required
def favoritesearch():
    tempJson = []
    suggestwordinput = request.form.get("suggestwordinput")
    if suggestwordinput != "":
        inputword = suggestwordinput
    else:
        inputword = request.form.get("inputword")
    favorites = Favorite.query.filter(Favorite.userID == current_user.id).all()
    for i in favorites:
        tempJson.append([i.id,
                         i.foodTitle,
                         i.foodPicture])
    df = pd.DataFrame(tempJson, columns=["id", "foodTitle", "foodPicture"])
    data = favoritesearchtfidf(inputword,df)
    suggestword = wordsuggestion(inputword)
    suggestwordreturn = ""
    if suggestword != inputword:
        suggestwordreturn = suggestword
    return render_template('favorite.html', data=data , userid=current_user.id,suggestword=suggestwordreturn,inputword=inputword)




