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

## Inserting Users
## Creating Users with No Content

# user = {
#         'User_Name' : "MollySmith",
#         'User_Email' : "mollys@gmail.com",
#         'User_Password' : 'password',
#         'First_Name'    : 'Molly',
#         'Last_Name'     : 'Smith'
#     }

# result=db.tracker.insert_one(user)
# print(result)

# users = [{
#         'User_Name' : "GumGum",
#         'User_Email' : "Luffy@gmail.com",
#         'User_Password' : 'password',
#         'First_Name'    : 'MonkeyD',
#         'Last_Name'     : 'Luffy'
#     },
#     {
#         'User_Name' : "Zoro",
#         'User_Email' : "Zoro@gmail.com",
#         'User_Password' : 'password',
#         'First_Name'    : 'Roronoa',
#         'Last_Name'     : 'Zoro'
#     },
#     {
#         'User_Name' : "Chopper",
#         'User_Email' : "Chopper@gmail.com",
#         'User_Password' : 'password',
#         'First_Name'    : 'TonyTony',
#         'Last_Name'     : 'Chopper'
#     }
#     ]

# result=db.tracker.insert_many(users)
# print(result)

## Creating Users with Content

# users = [
#  {
#     "User_Name"         : "Jane Austen",
#     "User_Email"        : "JaneAusten@gmail.com",
#     "User_Password"     : "test_password",
#     "First_Name"        : "Jane",
#     "Last_Name"         : "Austen",
#     "Content"           : [
#       {
#         "Title"           : "Pride and Prejudice",
#         "Release_Date"    : {
#             "$date": {
#               "$numberLong": "20150201T000000-0500"
#             }
#         },
#         "Type"              : "Book",
#         "Rating"            : 9,
#         "Genre"             : "Classic",
#         "Notes"             : "Mr. Darcy yes",
#         "Artwork"           : "TBD-should be an image not a string",
#         "Links"             : "User Content Links Go Here" 
#       },{
#       "Title"           : "Emma",
#       "Release_Date"    : {
#           "$date": {
#             "$numberLong": "20101110T000000-0500"
#           }
#       },
#       "Type"              : "Book",
#       "Rating"            : 10,
#       "Genre"             : "Classic",
#       "Notes"             : "Queen",
#       "Artwork"           : "TBD-should be an image not a string",
#       "Links"             : "User Content Links Go Here" 
#       }
#     ]
#   },
# {
#     "User_Name"         : "Emma",
#     "User_Email"        : "EmmaWatson@gmail.com",
#     "User_Password"     : "test_password",
#     "First_Name"        : "Emma",
#     "Last_Name"         : "Watson",
#     "Content"           : [
#       {
#         "Title"           : "Little Women",
#         "Release_Date"    : {
#             "$date": {
#               "$numberLong": "20051205T000000-0500"
#             }
#         },
#         "Type"              : "Book",
#         "Rating"            : 9,
#         "Genre"             : "Classic",
#         "Notes"             : "amazing",
#         "Artwork"           : "TBD-should be an image not a string",
#         "Links"             : "User Content Links Go Here" 
#       }
#     ]
#   }
# ]

# x = db.tracker.insert_many(users)

# #print list of the _id values of the inserted documents:
# print(x.inserted_ids)

## Adding New Content
## no content exists so has to be an array

# newValues = {'$set': {'Content':[{'Title': 'Legally Blonde', 'Type':'Movie', 'Rating':10}]}}
# result = db.tracker.update_one({'User_Name' : 'MollySmith'}, newValues)

## Adding Additional Content 
## There is content that exists, so does not an array

# newValues = {'$push':{'Content':{'Title': 'Avatar' , 'Type':'Movie', 'Rating':8}}}
# result = db.tracker.update_one({'User_Name' : 'MollySmith'}, newValues)
# newValues = {'$push':{'Content':{'Title': 'Megan' , 'Type':'Movie', 'Rating':2}}}
# result = db.tracker.update_one({'User_Name' : 'MollySmith'}, newValues)
# newValues = {'$push':{'Content':{'Title': 'Babylon' , 'Type':'Movie', 'Rating':5}}}
# result = db.tracker.update_one({'User_Name' : 'MollySmith'}, newValues)
# newValues = {'$push':{'Content':{'Title': 'Puss and Boots' , 'Type':'Movie', 'Rating':9}}}
# result = db.tracker.update_one({'User_Name' : 'MollySmith'}, newValues)
# newValues = {'$push':{'Content':{'Title': 'NYCVlog' , 'Type':'Youtube', 'Rating':8}}}
# result = db.tracker.update_one({'User_Name' : 'MollySmith'}, newValues)
# newValues = {'$push':{'Content':{'Title': 'FashionVlog' , 'Type':'Youtube', 'Rating':7}}}
# result = db.tracker.update_one({'User_Name' : 'MollySmith'}, newValues)
# newValues = {'$push':{'Content':{'Title': 'Pachinko' , 'Type':'Book', 'Rating':10}}}
# result = db.tracker.update_one({'User_Name' : 'MollySmith'}, newValues)
# newValues = {'$push':{'Content':{'Title': 'East of Eden' , 'Type':'Book', 'Rating':10}}}
# result = db.tracker.update_one({'User_Name' : 'MollySmith'}, newValues)
# newValues = {'$push':{'Content':{'Title': 'Breaking Bad' , 'Type':'TV', 'Rating':9}}}
# result = db.tracker.update_one({'User_Name' : 'MollySmith'}, newValues)
# newValues = {'$push':{'Content':{'Title': 'Family Guy' , 'Type':'TV', 'Rating':5}}}
# result = db.tracker.update_one({'User_Name' : 'MollySmith'}, newValues)
# newValues = {'$push':{'Content':{'Title': 'Community' , 'Type':'TV', 'Rating':6}}}
# result = db.tracker.update_one({'User_Name' : 'MollySmith'}, newValues)

## Querying
from bson import json_util

## List All Contents of a User
result = db.tracker.find({"User_Name": "MollySmith"}, 
                         {"_id": 0, "User_Name": 0, "User_Email":0,"User_Password":0, "First_Name":0, "Last_Name":0})
print(json_util.dumps(result, indent=2))

## List all Ratings of a User
result = db.tracker.find({"User_Name": "MollySmith"}, {"Content.Rating"})
print(json_util.dumps(result, indent=2))