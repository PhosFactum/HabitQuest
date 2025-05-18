# config.py
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
DB_PATH = os.getenv("DB_PATH")
