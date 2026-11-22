import json
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