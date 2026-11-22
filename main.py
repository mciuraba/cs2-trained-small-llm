import requests
import json
import sqlite3
from src.storage.database import *
from src.processing.data_operations import parse_json_messages, amount_of_messages_in_file, get_count_from_dict

BASE_URL = 'https://cs2tracker.gg/api/player/chat-log'



create_database()
connection = sqlite3.connect("data/cs2.db")

# ingesting loop
try:
    cur = connection.cursor()

    d = remove_spam_messages(connection)
    print(d)
except Exception:
        connection.rollback()
        raise
finally:
      connection.close()