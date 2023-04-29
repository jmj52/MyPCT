from flask import Blueprint, render_template, redirect, url_for, request, session
import pandas as pd
from website.extensions import mongo
from flask import session
from datetime import datetime

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
    error_sts = ''

    user_email = session.get('User_Email')
    content_item = request.form.get('add-content')
    
    print(f'\nadd-content:{content_item}')
    empty_dict = {'Title':' ','Release_Date':' ','Type':' ','Rating':' ','Genre':' ','Notes':' ','Links':' '}

    # POST runs when user selects Save Changes
    if request.method == 'POST':
        content_item = request.form.getlist('add-content')

        content_dict = {}
        for i,k in enumerate(list(empty_dict.keys())):
            content_dict[k] = content_item[i]
    
        print(f'content_dict: {content_dict}')
        if content_dict.get('Title') == '':
            error_sts = 'Error cannot have blank title'
            print(error_sts)
            return render_template('add_content.html',content_selected = empty_dict, error_sts = error_sts)


        # Update Database           
        query = {'User_Email':user_email}
        change = {'$push':{'Content':
                           {'Title':            content_item[0],        # String
                            'Release_Date':     content_item[1],        # Datetime       
                            'Type':             content_item[2],        # String
                            'Rating':           content_item[3],        # Int32
                            'Genre':            content_item[4],        # String
                            'Notes':            content_item[5],        # String
                            'Links':            content_item[6],        # String
                           }                     
                           }}

        mypct_cln.update_one(filter=query,update=change)
        return redirect(url_for('views.home'))

    return render_template('add_content.html',content_selected = empty_dict, error_sts = error_sts)


@views.route('/sel_content/<content_index>')
def sel_content(content_index):
    print(f'\nsel_content\n')
    session['user_selection'] = content_index
    return redirect(url_for('views.edit_content'))


@views.route('/edit_content', methods=['GET', 'POST'])
def edit_content():
    print(f'\nedit_content:{request.method}\n')
    error_sts = ''    

    supported_fields = ['Title','Release_Date','Type','Rating','Genre','Notes','Links']
    num_supported_fields=len(supported_fields)
    mypct_cln = mongo.cx.mypct.tracker
    
    # Get current content selected
    content_index = session.get('user_selection')
    selection_idx = int(content_index)-1
    
    # Get current User_Email selected
    user_email = session.get('User_Email')
    query = {'User_Email':user_email}
    record = mypct_cln.find(query)

    # Get content from data retrieved
    df = pd.DataFrame.from_records(record)
    user_content_data = df['Content'][0]

    # Use index of selected content to show content
    user_content_data_sel = user_content_data[selection_idx]
    current_content_title = user_content_data_sel['Title']

    #Remove Artwork from results
    remove_key = 'Artwork'
    if remove_key in user_content_data_sel: user_content_data_sel.pop(remove_key)

    # Translate raw data into standard template
    user_content_dict = {}
    for i,field in enumerate(supported_fields):
        if user_content_data_sel.get(field): 
            user_content_dict[field] = user_content_data_sel.get(field)
        else:
            user_content_dict[field] = ''

    # POST runs when user selects Save Changes
    if request.method == 'POST':
        content_item = request.form.getlist('edit-content')
        print('user_content_dict: ',user_content_dict)

        # Check to see if saved changes are different than existing content
        keys_to_update = {}
        keys = list(user_content_dict.keys())
        for i in range(0,len(user_content_dict)):
            existing_value  = list(user_content_dict.values())[i]
            new_value       = content_item[i]
            if new_value != '' and existing_value != new_value:
                print('change detected for',keys[i])
                keys_to_update.update({keys[i]:new_value})
            else:
                keys_to_update.update({keys[i]:existing_value})

        #print('keys_to_update:', keys_to_update)

        # Build empty frame and add only non-empty fields 
        updated_content = ['']*num_supported_fields
        test_dict = {}
        for i,k in enumerate(supported_fields):
            if keys_to_update.get(k):
                updated_content[i] = keys_to_update[k]
                test_dict[k] = keys_to_update[k]

        print(f'updated_content: {updated_content}')
        print(f'test_dict: {test_dict}')

        # Some Logic or Rules to validate various fields
        content_valid = True

        # Check for invalid datatype
        if test_dict.get('Title')        and not(isinstance(test_dict['Title'],         str)):
            content_valid = False
        # Checks disabled on datetime
        # if test_dict.get('Release_Date') and not(isinstance(test_dict['Release_Date'],  datetime)):
        #     error_sts = 'Release Date field is not a date'
        #     content_valid = False
        if test_dict.get('Type')         and not(isinstance(test_dict['Type'],          str)):
            error_sts = 'Type field is not a string'
            content_valid = False
        if test_dict.get('Rating')       and not(test_dict['Rating'].isnumeric()):
            error_sts = 'Rating field is not a numeric value'
            content_valid = False
        if test_dict.get('Genre')        and not(isinstance(test_dict['Genre'],         str)):
            error_sts = 'Genre field is not a string'
            content_valid = False
        if test_dict.get('Notes')        and not(isinstance(test_dict['Notes'],         str)):
            error_sts = 'Notes field is not a string'
            content_valid = False
        if test_dict.get('Links')        and not(isinstance(test_dict['Links'],         str)):
            error_sts = 'Link field is not a string'
            content_valid = False

        # Content Is Not Valid, return to edit page with original content
        if not(content_valid):
            return render_template('edit_content.html',content_selected = user_content_dict, error_sts = error_sts)
    
        # Content Is Valid, update database and return to content page
        else:
            query = {'User_Email':user_email,'Content.Title':current_content_title}
            
            change = {'$set':
                    {'Content.$.Title':           updated_content[0],      # String
                    'Content.$.Release_Date':    updated_content[1],      # Datetime       
                    'Content.$.Type':            updated_content[2],      # String
                    'Content.$.Rating':          int(updated_content[3]), # Int32
                    'Content.$.Genre':           updated_content[4],      # String
                    'Content.$.Notes':           updated_content[5],      # String
                    'Content.$.Links':           updated_content[6],      # String       
                        }}
            
            mypct_cln.update_one(filter=query,update=change)
            
            return redirect(url_for('views.home'))
        

    print(user_content_dict)
    return render_template('edit_content.html',content_selected = user_content_dict, error_sts=error_sts)


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


@views.route('/delete_content')
def delete_content():
    print(f'\ndelete_content\n')

    mypct_cln = mongo.cx.mypct.tracker

    # Get current content selected
    content_index = session.get('user_selection')
    selection_idx = int(content_index)-1

    # Get current User_Email selected
    user_email = session.get('User_Email')
    query = {'User_Email':user_email}
    record = mypct_cln.find(query)

    # Get content from data retrieved
    df = pd.DataFrame.from_records(record)
    user_content_data = df['Content'][0]

    # Use index of selected content to show content
    user_content_data_sel = user_content_data[selection_idx]
    current_content_title = user_content_data_sel['Title']
    change = {'$pull':{'Content':{'Title': current_content_title}}}
    mypct_cln.update_one(filter=query,update=change)

    return redirect(url_for('views.home'))


@views.route('/delete_all')
def delete_all():
    print(f'\ndelete_all\n')

    mypct_cln = mongo.cx.mypct.tracker

    # Get current User_Email selected
    user_email = session.get('User_Email')
    query = {'User_Email':user_email}
    record = mypct_cln.find(query)

    # Get content from data retrieved
    df = pd.DataFrame.from_records(record)
    user_content_data = df['Content'][0]

    # Delete each piece of content by title
    for content in user_content_data:
        current_content_title = content['Title']
        change = {'$pull':{'Content':{'Title': current_content_title}}}
        mypct_cln.update_one(filter=query,update=change)

    return redirect(url_for('views.home')) 


@views.route('/about')
def about():
    print(f'\nabout\n')
    return render_template('about.html')


