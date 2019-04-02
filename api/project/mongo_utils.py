from pymongo import MongoClient
import config

client = MongoClient()
client = MongoClient(config.mongo_host)
db = client[config.mongo_db]

bastidores = db.bastidores
slots = db.slots
patines = db.patines
users = db.users
rents = db.rents
