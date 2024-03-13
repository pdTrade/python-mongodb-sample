
from pymongo import MongoClient
from bson.objectid import ObjectId

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
  
def find_all():
  collection = test_db.test
  docs = collection.find()

  for doc in docs:
    print(doc)

def find_by_name():
  collection = test_db.test
  doc = collection.find_one({"first_name": "fname2"})

  print(doc)

def count_all():
  collection = test_db.test
  count = collection.count_documents({})

  print(count)
  
def find_by_id(id):
  _id = ObjectId(id)

  collection = test_db.test
  doc = collection.find_one({"_id": _id})

  print(doc)

def find_between(min, max):
  query = {
    "$and": [
      {"age": {"$gte": min}},
      {"age": {"$lte": max}},
  ]}

  collection = test_db.test
  docs = collection.find(query).sort("age")

  for doc in docs:
    print(doc)



find_between(20, 40)
