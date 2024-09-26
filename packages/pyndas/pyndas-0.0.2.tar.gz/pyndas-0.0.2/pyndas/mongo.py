from pymongo import MongoClient

class MongoDB:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, collection):
        return self.db[collection]

    def fetch_data(self,collection_name):
        collection = self.db[collection_name]
        return list(collection.find())

    def insert_data(self, collection_name, data):
        collection = self.get_collection(collection_name)
        collection.insert_one(data)