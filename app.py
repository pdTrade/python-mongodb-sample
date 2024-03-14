
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

def find_columns():
  columns = {"_id": 1, "first_name": 1}

  collection = test_db.test
  docs = collection.find({}, columns)

  for doc in docs:
    print(doc) 

def update_by_id(id):
  _id = ObjectId(id)
  collection = test_db.test 

  data = {
    "$rename": {"first_name": "aaa"},
    "$inc": {"age": 1},
    "$set": {"new_field": True}
  }
  collection.update_one({"_id": _id}, data)

  data = {
    "$unset": {"new_field": ""}
  }
  collection.update_one({"_id": _id}, data)

def replace_by_id(id):
  _id = ObjectId(id)
  collection = test_db.test 

  data = {
    "first_name": "f1",
    "last_name": "l1",
  }
  collection.replace_one({"_id": _id}, data)


def delete_by_id(id):
  _id = ObjectId(id)
  collection = test_db.test 

  collection.delete_one({"_id": _id})


def add_embed(id, data):
  _id = ObjectId(id)
  collection = test_db.test 

  collection.update_one({"_id": _id}, {"$addToSet": {"data": data}})

add_embed("65f19bc95d85963c3530ae90", {"a":2})
