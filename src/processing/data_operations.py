import json
import sqlite3
import string
from collections import defaultdict

def parse_json_messages(raw_data_path: str) -> list[dict]:
    with open(raw_data_path, "r", encoding="utf-8") as raw:
        data = json.load(raw)

    return parse_api_messages(data)


def amount_of_messages_in_file(raw_data_path: str) -> int:
    """
    Returns the amount of messages in json file from cstracker.gg
    """
    n_of_messages = 0
    with open(raw_data_path, "r", encoding="utf-8") as raw:
        data = json.load(raw)

    for match in data["matches"]:
        for message in match["messages"]:
            n_of_messages+=1
    return n_of_messages


def parse_api_messages(data: dict) -> list[dict]:
    messages = []

    for match in data["matches"]:
        for message in match["messages"]:
            messages.append(
                {
                    "steamid64": message["steamid64"],
                    "name": message["name"],
                    "text": message["text"],
                    "team": message["team"],
                    "round": message["round"],
                    "seq": message["seq"],
                    "played_at": match["playedAt"],
                    "share_code": match["shareCode"],
                    "map": match["map"],
                }
            )

    return messages

def analyze_words_from_db(db_path: str) -> dict:
    words = defaultdict(int)

    connection = sqlite3.connect(db_path)
    cur = connection.cursor()

    cur.execute("SELECT text FROM messages")

    for (text, ) in cur.fetchall():
        if not text:
            continue

        for word in text.lower().split():
            words[word] +=1

    connection.close()

    return words

def remove_words_from_dict(d: dict) -> dict:
    stop_words_list = {
        "the", "you", "gg", "your", "is",
        "are", "and", "i", "gh", "on", "to",
        "with", "my", "si", "tu", "of", "we",
        "ur", "when", "has", "have", "by",
        "ich", "на", "very", "hes", "but",
        "er", "its", "я", "didnt", "would",
        "would've", "should", "they", "us", "me",
        "in", "go", "a", "u", "3", "it", "so", "no", "d", "he", "this", "was", "wasnt", "that"
    }

    result = defaultdict(int)

    for word, count in d.items():
        cleaned_word = word.lower().strip(string.punctuation)

        if cleaned_word and cleaned_word not in stop_words_list:
            result[cleaned_word] += count

    return dict(result)

def get_count_from_dict(d: dict, word: str) -> int:

    if word in d:
        return d[word]

    return 0



