from flask import Blueprint, render_template, redirect, url_for, request, session
from bson.objectid import ObjectId
import pandas as pd
from website.extensions import mongo
from jinja2 import Environment
from flask import session

# Returns all records for a given username
def get_user_docs(a_collection, a_username):
    query = a_collection.find({'User_Name':a_username})
    return pd.DataFrame.from_records(query)

views = Blueprint('views',__name__)

@views.route('/')
def home():
    user_email = session.get('User_Email')
    if user_email is None:
        return redirect(url_for('auth.login'))

    mypct_cln = mongo.cx.mypct.tracker
    contents = mypct_cln.find({"User_Email": user_email}, {"_id": 0, "Content": 1})
    
    print(contents)
    return render_template('index.html', contents=contents)
    

@views.route('/add_content', methods=['GET', 'POST'])
def add_content():
    print(f'\nadd_content:{request.method}\n')
    mypct_cln = mongo.cx.mypct.tracker

    content_item = request.form.get('add-content')
    
    print(f'\nadd-content:{content_item}')

    # POST runs when user selects Save Changes
    if request.method == 'POST':
        content_item = request.form.getlist('add-content')
        print('content-passed:',content_item)

        #mypct_cln.insert_one({'text': content_item})

    empty_dict = {'Title:':' ','Release_Date':' ','Type':' ','Rating':' ','Genre':' ','Notes':' ','Links':' '}
    return render_template('edit_content.html',content_selected = empty_dict, op = 'Add')


@views.route('/sel_content/<content_index>')
def sel_content(content_index):
    print(f'\nsel_content\n')
    session['user_selection'] = content_index
    return redirect(url_for('views.edit_content'))

@views.route('/edit_content', methods=['GET', 'POST'])
def edit_content():
    print(f'\nedit_content:{request.method}\n')
    mypct_cln = mongo.cx.mypct.tracker
    
    # Get current content selected
    content_index = session.get('user_selection')
    selection_idx = int(content_index)-1
    print('selection_idx:',selection_idx)
    
    # Get current User_Email selected
    user_email = session.get('User_Email')
    print(user_email)
    query = {'User_Email':user_email}
    record = mypct_cln.find(query)

    # Get content from data retrieved
    df = pd.DataFrame.from_records(record)
    user_content_data = df['Content'][0]

    # Use index of selected content to show content
    user_content_data_sel = user_content_data[selection_idx]
    #print(f'\nuser_data:\n{user_content_data_sel}')

    current_content_title = user_content_data_sel['Title']

    #Remove Artwork from results
    remove_key = 'Artwork'
    if remove_key in user_content_data_sel: user_content_data_sel.pop(remove_key)

    # POST runs when user selects Save Changes
    if request.method == 'POST':
        content_item = request.form.getlist('edit-content')
        print('content-passed:',content_item)

        # Assume Content Is Not Valid until we can validate the user input
        # Override to true for now, no validation criteria setup
        content_valid = True

        # Some Logic or Rules to validate various fields

        # Content Is Not Valid, return to edit page with original content
        if not(content_valid):
            return render_template('edit_content.html',content_selected = user_content_data_sel)

        # Content Is Valid, update database and return to content page
        else:
            
            # Update Database
            fields = list(user_content_data_sel.keys())
            
            query = {'_id':ObjectId(current_user_id),'Content.Title':current_content_title}
            
            change = {'$set':
                      {'Content.$.Title':           content_item[0],
                       'Content.$.Release_Date':    content_item[1],       
                       'Content.$.Type':            content_item[2],
                       'Content.$.Rating':          content_item[3],
                       'Content.$.Genre':           content_item[4],
                       'Content.$.Notes':           content_item[5],      
                       'Content.$.Links':           content_item[6],       
                        }}
            
            mypct_cln.update_one(filter=query,update=change)
            
            return redirect(url_for('views.home'))
        

    # show the form, it wasn't submitted
    return render_template('edit_content.html',content_selected = user_content_data_sel, op = 'Edit')

@views.route('/sort_content')
def sort_content():
    print(f'\nsort_content\n')
    user_email = session.get('User_Email')
    if user_email is None:
        return redirect(url_for('auth.login'))

    mypct_cln = mongo.cx.mypct.tracker
    contents = mypct_cln.find({"User_Email": user_email}, {"_id": 0, "Content": 1})
    

    # Display sorted content
    sorting_methods = ['Unsorted','Rating','Title']
    sort_method = session.get('Sort_Method')
    sort_method_idx = sorting_methods.index(sort_method)

    #print('sort_method:',sort_method)

    # Sort content if sort method is not default/unsorted value
    if sort_method != 'Unsorted':
        content_frame = pd.DataFrame.from_records(contents.__copy__())['Content'][0]
        if sort_method == 'Rating':
            contents = sorted(content_frame, key=lambda d: d.get(sort_method, 0), reverse=True)
        elif sort_method == 'Title':
            contents = sorted(content_frame, key=lambda d: d.get(sort_method, 'zzzzzz'))
        else:
            # Default case - should not be encountered
            pass

        sort_method_str = ' by ' + sort_method
    else:
        sort_method_str = ''

    # Toggle sort method
    if sort_method_idx < len(sorting_methods)-1:
        sort_method_idx += 1
    else:
        sort_method_idx = 0

    session['Sort_Method'] = sorting_methods[sort_method_idx]
    return render_template('index.html', contents=contents, method=sort_method_str)
    
    
@views.route('/cancel_changes')
def cancel_changes():
    print(f'\ncancel_changes\n')
    return redirect(url_for('views.home'))

# TODO: Add delete content functionality
@views.route('/delete_content')
def delete_content():
    print(f'\ndelete_content\n')
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


@views.route('/about')
def about():
    print(f'\nabout\n')
    return render_template('about.html')


