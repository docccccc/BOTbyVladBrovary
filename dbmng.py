from pymongo import MongoClient
from config import MONGO_CONN

cluster = MongoClient(MONGO_CONN)

db = cluster['Bot_Wallet']

coll = db['User_aspine']

curer = db['Kur']