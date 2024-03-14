
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime as dt
from pprint import pprint

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


def create_data():
  authors = [
    {
      "first_name": "f1",
      "last_name": "l1",
      "date_of_birth": dt(2001, 1, 10)
    },
    {
      "first_name": "f2",
      "last_name": "l2",
      "date_of_birth": dt(2001, 2, 10)
    },
    {
      "first_name": "f3",
      "last_name": "l3",
      "date_of_birth": dt(2001, 3, 10)
    },
    {
      "first_name": "f4",
      "last_name": "l4",
      "date_of_birth": dt(2001, 4, 10)
    },
    {
      "first_name": "f5",
      "last_name": "l5",
      "date_of_birth": dt(2001, 5, 10)
    },
  ]

  author_collection = test_db.author 
  ids = author_collection.insert_many(authors).inserted_ids

  books = [
    {
      "title": "t1",
      "authors": [ids[0]],
      "publish_date": dt(2001, 1, 10),
      "type": "fiction",
      "copies": 1
    },
    {
      "title": "t2",
      "authors": [ids[1]],
      "publish_date": dt(2002, 2, 10),
      "type": "fiction",
      "copies": 2
    },
    {
      "title": "t3",
      "authors": [ids[2]],
      "publish_date": dt(2003, 3, 10),
      "type": "non-fiction",
      "copies": 3
    },
    {
      "title": "t4",
      "authors": [ids[3]],
      "publish_date": dt(2004, 4, 10),
      "type": "non-fiction",
      "copies": 4
    },
    {
      "title": "t5",
      "authors": [ids[4]],
      "publish_date": dt(2005, 5, 10),
      "type": "fiction",
      "copies": 5
    },
  ]

  book_collection = test_db.book 
  book_collection.insert_many(books)


authors_and_books = test_db.author.aggregate([{
  "$lookup": {
    "from": "book",
    "localField": "_id",
    "foreignField": "authors",
    "as": "books"
  }
}])

authors_book_count = test_db.author.aggregate([
  {
    "$lookup": {
      "from": "book",
      "localField": "_id",
      "foreignField": "authors",
      "as": "books"
    }
  },
  {
    "$addFields": {
      "total_books": {"$size": "$books"}
    } 
  },
  { 
    "$project": {
      "first_name": 1,
      "last_name": 1,
      "total_books": 1,
      "_id": 0
    }
  }
])

books_with_old_authors = test_db.book.aggregate([
  {
    "$lookup": {
      "from": "author",
      "localField": "authors",
      "foreignField": "_id",
      "as": "authors"
    }
  },
  {
    "$set": {
      "authors": {
        "$map": {
          "input": "$authors",
          "in": {
            "first_name": "$$this.first_name",
            "last_name": "$$this.last_name",
            "age": {
              "$dateDiff": {
                "startDate": "$$this.date_of_birth",
                "endDate": "$$NOW",
                "unit": "year"
              }
            }
          }
        }
      }
    }
  }
])

pprint(list(books_with_old_authors))