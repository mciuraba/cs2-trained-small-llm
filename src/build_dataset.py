import sqlite3

from src.storage.database import get_messages_in_order
from src.dataset.dataset_builder import export_to_jsonl


def main():
    connection = sqlite3.connect("data/cs2.db")

    try:
        matches = get_messages_in_order(connection)

        print(f"Loaded matches: {len(matches)}")

        export_to_jsonl(
            matches,
            "data/processed/conversations.jsonl"
        )

        print("Dataset exported successfully!")

    finally:
        connection.close()


if __name__ == "__main__":
    main()