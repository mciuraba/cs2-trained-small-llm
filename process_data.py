import json
from collections import defaultdict

def make_jsonl_file_with_messages(raw_data_path: str, count = 0) -> str:
    '''
    Returns the jsonl path of the created file
    '''
    with open(raw_data_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    total_messages = 0
    final_path = f"messages_{count}.jsonl"

    with open(final_path, "w", encoding="utf-8") as file:

        for match in data["matches"]:
            for message in match["messages"]:

                record = {
                    "steamid64": message["steamid64"],
                    "name": message["name"],
                    "text": message["text"],
                    "team": message["team"],
                    "round": message["round"],
                    "seq": message["seq"],
                    "played_at": match["playedAt"],
                    "share_code": match["shareCode"],
                    "map": match["map"],
                    "message_id": (match["shareCode"], message["seq"])
                }

                file.write(json.dumps(record, ensure_ascii=False) + "\n")
                total_messages += 1

    return final_path

def deduplicate(jsonl_data):
    seen_messages = set()
    messages_count = 0
    with open(jsonl_data, "r", encoding="utf-8") as source:
        with open("unique_messages.jsonl", "w", encoding="utf-8") as destination:
            for line in source:
                message = json.loads(line)
                message_id = (message["share_code"], message["seq"])

                if message_id not in seen_messages:
                    seen_messages.add(message_id)
                    destination.write(line)
                messages_count+=1

    print("Messages count before: ", messages_count)
    print("Unique messages: ", len(seen_messages))
    print("Duplicates removed:", messages_count - len(seen_messages))

def analyze_words(jsonl_data):
    # dla przechowania ilości słow, kazde slowo na male litery!
    messages_dictionary = defaultdict(int)

    with open(jsonl_data, "r", encoding="utf-8") as file:
        for line in file:
            message = json.loads(line)
            text = message["text"].lower()
            words = text.split()

            for word in words:
                messages_dictionary[word] +=1

    return messages_dictionary

def remove_stop_words_from_dict(d) -> dict:
    stop_words_list = ["the", "you", "gg", "your", "is", "are", "and", "i", "gh", "on", "to"]

    for word in stop_words_list:
        d[word] = 0

    return d




