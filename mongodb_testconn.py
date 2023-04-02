### Joshua Jones                    ###
### Testing Connection to MongoDB   ###

#--- Required installs ---#
# pip install pymongo
# pip install dnspython

from pymongo import MongoClient
import certifi
from pprint import pprint
import pandas as pd
from bson.objectid import ObjectId



# Returns all records for a given username
def get_user_docs(a_collection, a_username):
    query = a_collection.find({'User_Name':a_username})
    return pd.DataFrame.from_records(query)


def main():
    # Connect to MongoDB server
    mongodb_url = "mongodb+srv://joshua:joshuajoshua@cluster0.cgmpycw.mongodb.net/test"
    client      = MongoClient(mongodb_url, tlsCAFile=certifi.where())

    # List Available Databases - TODO: REMOVE - FOR TESTING ONLY
    # db_names = client.list_database_names()
    # print(db_names)

    # Select database
    mypct_db = client.get_database('mypct')

    # List collections - TODO: REMOVE - FOR TESTING ONLY
    # mypct_cln_all = mypct_db.list_collection_names()
    # print(mypct_cln_all)

    # Select collection
    mypct_cln = mypct_db['tracker']

    #print(mypct_db.tracker.find_one())
    
    ### Queries ###

    # Get all records from a specific user
    # username = 'test_user'
    # records = get_user_docs(mypct_cln, username)
    #print(records.head())

    # Delete all 
    # mypct_cln.delete_many({})
    # exit()

    # Edit Content
    current_user_id = "64223e0a2529c24efa6f4701"
    current_content_title = 'Inserted Title'
    edited_content_title  = 'Revised Title'
    query = {'_id':ObjectId(current_user_id),'Content.Title':current_content_title}
    change = {'$set':{'Content.$.Title':edited_content_title}}
    mypct_cln.update_one(filter=query,update=change)

    query = {'_id':ObjectId(current_user_id)}
    record = mypct_cln.find(query)
    df = pd.DataFrame.from_records(record)
    print(df)
    exit()

    # Add Content
    current_user_id = "64223e0a2529c24efa6f4701"
    current_content_title = 'Inserted Title'
    query = {'_id':ObjectId(current_user_id)}
    change = {'$push':{'Content':{'Title': current_content_title}}}
    mypct_cln.update_one(filter=query,update=change)

    record = mypct_cln.find(query)
    df = pd.DataFrame.from_records(record)
    print(df)

    # Delete Content
    current_user_id = "64223e0a2529c24efa6f4701"
    current_content_title = 'This Is A Title'
    query = {'_id':ObjectId(current_user_id)}
    change = {'$pull':{'Content':{'Title': current_content_title}}}
    mypct_cln.update_one(filter=query,update=change)
    
    record = mypct_cln.find(query)
    df = pd.DataFrame.from_records(record)
    print(df)

if __name__ == '__main__':
    main()

##### Kenzie Lee (Mackenzie Peddle) #####

db = client.mypct