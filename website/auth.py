from flask import Blueprint, render_template, request, session, redirect, url_for
from website import mongo
from website.extensions import mongo

auth = Blueprint('auth',__name__)

# Login Page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # gets email from user input
        email = request.form.get('email') 
        # gets password from user input
        password = request.form.get('password') 
        # finds if the user email exists in the database
        user = mongo.cx.mypct.tracker.find_one({'User_Email' : email}) 
        
        # if the user email exists
        if user:
            # if the password in the user email document matches the password the user entered 
            if user['User_Password'] == password:
                # creates a session for the user
                session['User_Email'] = email
                session['Sort_Method'] = 'Unsorted'
                # directions to the home page 
                return redirect(url_for('views.home'))
            else:
                return 'Incorrect password. Go back.'
        else:
            return 'Email does not exist. Go back.'
        
    return render_template('login.html')

# Logout Page
@auth.route('/logout')
def logout():
    # Ends the user session
    session.pop('User_Email', None)
    return redirect(url_for('auth.login'))

# Signup Page
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # retrieves the user's first and last name, email, and password
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # checks to see if the user email is in the database
        existing_user = mongo.cx.mypct.tracker.find_one({'User_Email' : email})
        
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        
        if len(password) < 3:
            return "Password must be longer than 2 characters. Go back."
        else:
            # if the user email does not exist
            if existing_user is None:
                # creates the user in the database in a document
                mongo.cx.mypct.tracker.insert_one({'First_Name': firstName, 'Last_Name': lastName, 'User_Email': email, 'User_Password': password})
                # creates a session for the user
                session['User_Email'] = email
                session['Sort_Method'] = 'Unsorted'
                return redirect(url_for('views.home'))

    return render_template('signup.html')