from dotenv import load_dotenv
import os
load_dotenv()
from pymongo import MongoClient

class MongoDB:
    conn = MongoClient(os.getenv('DB_URL_PROD'), ssl=True)
    database = conn[os.getenv('DATABASE')]