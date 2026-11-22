import requests
import json
import sqlite3
from src.storage.database import *
from src.processing.data_operations import parse_json_messages, amount_of_messages_in_file

BASE_URL = 'https://cs2tracker.gg/api/player/chat-log'



create_database()
connection = sqlite3.connect("data/cs2.db")

# ingesting loop
try:
    messages = parse_json_messages("data/raw/raw_data.json")
    ingest_messages(messages, connection)
    connection.commit()

    player = get_next_unprocessed_player(connection)
    print(player)

    mark_player_as_processed(player, connection)
    connection.commit()

    next_player = get_next_unprocessed_player(connection)
    print(next_player)

    match_messages = get_messages_in_order(connection=connection)
except Exception:
        connection.rollback()
        raise
finally:
      connection.close()