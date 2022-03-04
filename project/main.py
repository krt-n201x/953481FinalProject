from unittest import result
import pandas as pd
from flask import Blueprint, render_template, app, request
from flask_login import login_required, current_user
from . import dataexample, dataframe
from .models import Favorite
from .process import favoritesearchtfidf, wordsuggestion, findfooddetails, searchtfidf

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html', data=dataexample)

@main.route('/home')
@login_required
def homeindex():
    inputword = request.form.get("inputword")
    suggestwordreturn = ""
    return render_template('index.html', data=dataexample, userid=current_user.id,suggestword=suggestwordreturn,inputword=inputword)

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

@main.route('/searcall', methods=['POST'])
@login_required
def searcall():
    getin = request.form.get("getin")
    if getin:
        searcbyname = request.form.get("searcbyname")
        searcbyingredient = request.form.get("searcbyingredient")
        suggestword =""
        data =""
        result = ""
        inputword =""
        return render_template('searchall.html', userid=current_user.id , result=result,searcbyname=searcbyname, searcbyingredient=searcbyingredient,suggestword=suggestword,data=data)
    else:
        searcbyname = request.form.get("searcbyname")
        searcbyingredient = request.form.get("searcbyingredient")
        suggestwordinput = request.form.get("suggestwordinput")
        inputword = request.form.get("inputword")
        print(searcbyname,searcbyingredient,suggestwordinput,inputword)
        data =""
        if suggestwordinput != "":
            inputword = suggestwordinput
        else:
            inputword = request.form.get("inputword")
        if searcbyname:
            data = searchtfidf(inputword,dataframe,'Title')
        if searcbyingredient:
            data = searchtfidf(inputword,dataframe,'Ingredients')
        suggestwordreturn = ""
        suggestword = wordsuggestion(inputword)
        if suggestword != inputword:
            suggestwordreturn = suggestword

        result = 0
        for i in data:
            result = result+1
        print(result)

        return render_template('searchall.html',data=data, userid=current_user.id, searcbyname=searcbyname, searcbyingredient=searcbyingredient,suggestword=suggestwordreturn, result=result)

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




