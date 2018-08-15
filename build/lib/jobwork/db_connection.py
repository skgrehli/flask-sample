from pymongo import MongoClient
import pprint

__all__ = ['db']

client = MongoClient()  # connection
db = client.saveOnJobs

