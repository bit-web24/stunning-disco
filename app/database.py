import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.environ.get('DB_URL'))
db = client[os.environ.get('DB_NAME')]
users = db['users']
