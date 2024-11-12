from bson.objectid import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

class Database:
    def __init__(self, db_name: str):
        self.__client = MongoClient(os.environ.get('DB_URL'))
        self.__db = self.__client[db_name]        
        self.__collection = None

    def set_collection(self, collection_name: str):
        self.__collection = self.__db[collection_name]
        return self

    def insert(self, doc: dict):
        if self.__collection is None:
            raise Exception("Collection not set")

        doc['_id'] = ObjectId()
        result = self.__collection.insert_one(doc)
        inserted_doc = self.__collection.find_one({'_id': result.inserted_id})
        return inserted_doc

    def get_all(self):
        if self.__collection is None:
            raise Exception("Collection not set")
        return list(self.__collection.find())

    def get(self, query):
        if self.__collection is None:
            raise Exception("Collection not set")
        return self.__collection.find_one(query)

    def update(self, get_q, set_q):
        if self.__collection is None:
            raise Exception("Collection not set")
        return self.__collection.update_one(get_q, {'$set': set_q})

    def delete(self, query):
        if self.__collection is None:
            raise Exception("Collection not set")
        return self.__collection.delete_one(query)

    def close(self):
        self.__client.close()