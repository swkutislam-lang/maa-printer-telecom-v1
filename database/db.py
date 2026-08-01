import sqlite3
import os

DB_NAME = "database/shop.db"

os.makedirs("database", exist_ok=True)

def get_connection():
    return sqlite3.connect(DB_NAME)
