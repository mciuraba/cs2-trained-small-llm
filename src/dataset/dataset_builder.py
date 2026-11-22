import sqlite3
import string
import json


#connection = sqlite3.connect()


def group_messages_by_round(match: dict) -> list[dict]:
    rounds = {}

    for message in match["messages"]:
        round_number = message["round"]

        if round_number not in rounds:
            rounds[round_number] = []

        rounds[round_number].append(message)

    return [
        {
            "round": round_number,
            "messages": messages
        }
        for round_number, messages in sorted(rounds.items())
    ]

def round_sliding_window(rounds):
    windows = []

    for i in range(1, len(rounds) - 1):
        r1 = rounds[i-1]
        r2 = rounds[i]
        r3 = rounds[i+1]

        if r1["round"] + 1 == r2["round"] and r2["round"] + 1 == r3["round"]:
            windows.append([r1, r2, r3])

    return windows

def export_to_jsonl(matches, output_path):
    with open(output_path, "w", encoding="utf-8") as file:
        for match in matches:
            rounds = group_messages_by_round(match)
            windows = round_sliding_window(rounds)
            for window in windows:
                record = {
                    "share_code":match["share_code"],
                    "rounds":window
                }
                json_record = json.dumps(record, ensure_ascii=False)
                file.write(json_record + "\n")



