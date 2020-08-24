import pymongo
import random
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from spiders.settings import MONGO_HOST, MONGO_PORT


class Mongo_pool(object):
    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
        # client['db']['collection']
        self.collection = self.client['scenic_spots']['mafengwo']

    def __del__(self):       
        self.client.close()

    def insert_one(self, dic):       
        self.collection.insert_one(dic)

    def delete_one(self, obj):
        self.collection.delete_one({"_id": obj.name})

    def update_one(self, obj):
        self.collection.update_one({"_id": proxy.name}, {'$set': obj.__dict__})

    def find_all(self):
        cursor = self.collection.find()
        arr = []
        for item in cursor:
            arr.append(item)
        return arr

    def find_by_condition(self, condition={}, limit=0):
        cursor = self.collection.find(condition, limit=limit).sort([
            ('comments', pymongo.DESCENDING)
        ])
        arr = []
        for item in cursor:
            # item.pop('_id')
            # obj = proxy(**item)
            arr.append(item)

        return arr


mongo = Mongo_pool()
