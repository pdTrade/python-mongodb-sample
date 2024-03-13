
from pymongo import MongoClient

client = MongoClient('localhost', 27017)


dbs = client.list_database_names()
# print(dbs)

test_db = client.test
collections = test_db.list_collection_names()
# print(collections)

def insert_test_doc():
  collection = test_db.test
  test_doc = {
    "name": "name1",
    "type": "type1"
  }

  id = collection.insert_one(test_doc).inserted_id
  # print(id)

def create_documents():
  first_names = ['fname1', 'fname2', 'fname3', 'fname4', 'fname5']
  last_names = ['lname1', 'lname2', 'lname3', 'lname4', 'lname5']
  ages = [10, 20, 30, 40, 50]

  docs = []

  for first_name, last_name, age in zip(first_names, last_names, ages):
    doc = {"first_name": first_name, "last_name": last_name, "age": age}
    docs.append(doc)

  collection = test_db.test
  collection.insert_many(docs)
  


create_documents()