from flask import Blueprint, render_template, request, session, redirect, url_for
from website import mongo
from flask_pymongo import PyMongo

auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        existing_user = mongo.db.tracker.find_one({'User_Email' : email, 'User_Password': password})
        if existing_user is None:
            print("No Account Exists")
            return render_template('signup.html')
        return redirect(url_for('views.home'))
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return '<p>logout</p>'

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')
        
        existing_user = mongo.db.tracker.find_one({'User_email' : email})
        
        if existing_user is None:
            mongo.db.tracker.insert_one({'First_Name': firstName, 'Last_Name': lastName, 'User_Email': email, 'User_Password': password})
            session['User_Email'] = email
            return redirect(url_for('views.home'))
        
        return 'That email already exists!'
    
    return render_template('signup.html')