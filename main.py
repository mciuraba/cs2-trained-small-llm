import requests
import json
import sqlite3
from src.storage.database import create_database, add_player, add_message, get_messages_from_steamid, get_all_steamids, get_num_of_messages
from src.processing.data_operations import parse_json_messages, amount_of_messages_in_file

BASE_URL = 'https://cs2tracker.gg/api/player/chat-log'

# init db for players
create_database()

# get messages for testing
messages = parse_json_messages("data/raw/raw_data.json")

connection = sqlite3.connect("data/cs2.db")


for message in messages:
    add_message(message, connection)
connection.commit()



# amount_of_records = 0
# cur = connection.cursor()

# cur.execute(
#     "SELECT COUNT(*) FROM messages"
# )
# print(cur.fetchall())

# print(amount_of_messages_in_file("data/raw/raw_data.json"))


#message = get_messages_from_steamid("76561198171178965", connection)
#print(message)

# steamids = get_all_steamids(connection=connection)
# print(steamids)

n_of_mess = get_num_of_messages(connection=connection)
print(n_of_mess)

connection.close()