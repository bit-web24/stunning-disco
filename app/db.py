import os
from dotenv import load_dotenv
from app.utils.database import Database

load_dotenv()

db = Database(os.environ.get('DB_NAME'))
