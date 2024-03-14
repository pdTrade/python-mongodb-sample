
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('localhost', 27017)


dbs = client.list_database_names()
# print(dbs)

test_db = client.test
collections = test_db.list_collection_names()
# print(collections)

def create_book_collection():
  validator = {
    "$jsonSchema": {
       "required": [ "title", "authors", "publish_date", "type" ],
       "properties": {
          "title": {
             "bsonType": "string",
             "description": "must be a string and is required"
          },
          "authors": {
             "bsonType": "array",
             "items": {
               "bsonType": "objectId",
              "description": "must be an objectid and is required"
             }
          },
          "publish_date": {
             "bsonType": "date",
             "description": "must be a date and is required"
          },
          "type": {
             "enum": ["fiction", "non-fiction"],
             "description": "can only be one of the enum values and is required"
          },
          "copies": {
             "bsonType": "int",
             "minimum": 0,
             "description": "must be an integer greater than 0 and is required"
          },
       }
    }
  }

  try:
    test_db.create_collection("book")
  except Exception as e:
    print(e)

  test_db.command("collMod", "book", validator=validator)

def create_author_collection():

  validator = {
    "$jsonSchema": {
       "required": [ "first_name", "last_name", "date_of_birth" ],
       "properties": {
          "first_name": {
             "bsonType": "string",
             "description": "must be a string and is required"
          },
          "last_name": {
             "bsonType": "string",
             "description": "must be a string and is required"
          },
          "date_of_birth": {
             "bsonType": "date",
             "description": "must be a date and is required"
          },
       }
    }
  }

  try:
    test_db.create_collection("author")
  except Exception as e:
    print(e)

  test_db.command("collMod", "author", validator=validator) 


create_author_collection()
