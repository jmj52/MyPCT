### Joshua Jones                    ###
### Testing Connection to MongoDB   ###

#--- Required installs ---#
# pip install pymongo
# pip install dnspython

from pymongo import MongoClient
import certifi
from pprint import pprint
import pandas as pd


# Returns all records for a given username
def get_user_docs(a_collection,a_username):
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


    ### Queries ###

    # Get all records from a specific user
    username = 'test_user'
    records = get_user_docs(mypct_cln, username)
    print(records.head())



if __name__ == '__main__':
    main()

