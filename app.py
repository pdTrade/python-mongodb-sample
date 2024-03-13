
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
  print(id)

insert_test_doc()
