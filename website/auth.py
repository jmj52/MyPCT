from flask import Blueprint, render_template, request, session, redirect, url_for
from website import mongo
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = mongo.cx.mypct.tracker.find_one({'User_Email' : email})
        if user:
            # if check_password_hash(user['User_Password'], password):
            if user['User_Password'] == password:
                session['User_Email'] = email
                return redirect(url_for('views.home'))
            else:
                print('Incorrect password, try again.')
        else:
            print('Email does not exist.')
        
    return render_template('login.html')


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
        
        existing_user = mongo.cx.mypct.tracker.find_one({'User_Email' : email})
        
        if existing_user is None:
            #hashed = generate_password_hash(password, method='sha256')
            mongo.cx.mypct.tracker.insert_one({'First_Name': firstName, 'Last_Name': lastName, 'User_Email': email, 'User_Password': password})
            session['User_Email'] = email
            return redirect(url_for('views.home'))
        
        return 'That email already exists!'
    
    return render_template('signup.html')