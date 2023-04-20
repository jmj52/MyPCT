from flask import Blueprint, render_template, redirect, url_for, request
from bson.objectid import ObjectId
import pandas as pd
from website.extensions import mongo
from jinja2 import Environment
from flask import session

def len_filter(value):
    return len(value)

>>>>>>> Stashed changes


# Returns all records for a given username
def get_user_docs(a_collection, a_username):
    query = a_collection.find({'User_Name':a_username})
    return pd.DataFrame.from_records(query)

views = Blueprint('views',__name__)

@views.route('/')
def home():
    user_email = session.get('user_email')
    if user_email is None:
        return redirect(url_for('auth.login'))

    mypct_cln = mongo.cx.mypct.tracker
    contents = mypct_cln.find({"User_Email": user_email}, {"_id": 0, "Content": 1})
    
    return render_template('index.html', contents=contents)

##@views.route('/')
##def home():
    mypct_cln = mongo.cx.mypct.tracker
    contents = mypct_cln.find( { "User_Email": "JaneAusten@gmail.com" },{ "_id":0, "Content":1})
    return render_template('index.html',contents=contents)

@views.route('/add_content', methods=['POST'])
def add_content():
    mypct_cln = mongo.cx.mypct.tracker

    content_item = request.form.get('add-content')
    
    query = get_user_docs(mypct_cln,'test_user')
    print(query.head())
    current_content_title = 'Title Updated via Flask-add'
    query = {'User_Name':'test_user'}
    change = {'$push':{'Content':{'Title': current_content_title}}}
    mypct_cln.update_one(filter=query,update=change)

    #mypct_cln.insert_one({'text': content_item})
    print(content_item)
    return redirect(url_for('views.home'))

@views.route('/delete_completed', methods=['POST'])
def delete_completed():
    mypct_cln = mongo.cx.mypct.tracker
    mypct_cln.delete_many({'complete' : True})
    return redirect(url_for('views.home'))

@views.route('/delete_all', methods=['POST'])
def delete_all():
    pass

@views.route('/complete_content/<oid>')
def complete_content(oid):
    mypct_cln = mongo.cx.mypct.tracker
    content_item = mypct_cln.find_one({'_id': ObjectId(oid)})
    content_item['new'] = True



    current_content_title = 'This Is A Title'
    edited_content_title = 'Title Updated via Flask-completed'

    query = {'_id':ObjectId(oid),'Content.Title':current_content_title}
    change = {'$set':{'Content.$.Title':edited_content_title}}
    mypct_cln.update_one(filter=query,update=change)
    #mypct_cln.update_one(content_item)
    return redirect(url_for('views.home'))








