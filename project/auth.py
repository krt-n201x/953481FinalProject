from flask import Blueprint, render_template, redirect, url_for, request, flash, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User, Favorite
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user:
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    if not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)

    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    repassword = request.form.get('re-password')
    if email == "":
        flash('Please fill out the information completely.')
        return redirect(url_for('auth.signup'))
    if name == "":
        flash('Please fill out the information completely.')
        return redirect(url_for('auth.signup'))
    if password == "":
        flash('Please fill out the information completely.')
        return redirect(url_for('auth.signup'))
    if repassword == "":
        flash('Please fill out the information completely.')
        return redirect(url_for('auth.signup'))
    if password != repassword:
        flash('your password are not match')
        return redirect(url_for('auth.signup'))
    if user:
        flash('Email address already exists.')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/add-favorite', methods=["GET", "POST"])
def add_favorite():
    userID = request.form.get('userID')
    foodTitle = request.form.get('foodTitle')
    foodPicture = request.form.get('foodPicture')

    favorite = Favorite.query.filter_by(foodTitle=foodTitle,userID=userID).first()
    if favorite :
        flash(0)
        return redirect(url_for('main.homeindex'))

    new_favorite = Favorite(
        userID=userID,
        foodTitle=foodTitle,
        foodPicture=foodPicture
    )
    db.session.add(new_favorite)
    db.session.commit()

    flash(1)
    return redirect(url_for('main.homeindex'))

@auth.route('/delete-favorite', methods=["GET", "POST"])
def delete_favorite():
    userID = request.form.get('userID')
    foodTitle = request.form.get('foodTitle')
    try:
        delete_favorite = Favorite.query.filter(Favorite.foodTitle==foodTitle, Favorite.userID==userID).first()
        db.session.delete(delete_favorite)
        db.session.commit()
        return redirect(url_for('main.favorite'))
    except:
        return redirect(url_for('main.homeindex'))