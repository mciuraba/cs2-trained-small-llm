import sqlite3

from playwright.async_api import async_playwright

from src.downloading.cs2_tracker import fetch_player_matches
from src.processing.data_operations import parse_api_messages
from src.storage.database import (
    get_next_unprocessed_player,
    ingest_messages,
    mark_player_as_processed,
    get_num_of_players,
    get_num_of_processed_players,
    get_num_of_messages,
    remove_spam_messages
)

TARGET_MESSAGES = 300_000
MAX_PLAYERS = 3_000

async def process_next_player(connection: sqlite3.Connection, page):
    steamid64 = get_next_unprocessed_player(connection)

    if steamid64 is None:
        return False

    print(f"\nProcessing player: {steamid64}")

    try:
        data = await fetch_player_matches(page, steamid64)
        messages = parse_api_messages(data)

        ingest_messages(messages, connection)

        # Usuwamy spam po pobraniu danych gracza
        removed = remove_spam_messages(connection, threshold=7)

        mark_player_as_processed(steamid64, connection)
        connection.commit()

        print(f"Fetched: {len(messages)} messages")
        print(f"Spam removed: {removed}")
        print(f"Discovered matches: {len(data['matches'])}")
        print(f"Total players: {get_num_of_players(connection)}")
        print(f"Processed players: {get_num_of_processed_players(connection)}")
        print(f"Total messages: {get_num_of_messages(connection)}")

        return True

    except Exception:
        connection.rollback()
        raise

async def main():
    connection = sqlite3.connect("data/cs2.db")

    try:
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(
                "http://localhost:9222"
            )

            context = browser.contexts[0]

            page = next(
                (p for p in context.pages if "cs2tracker.gg" in p.url),
                None
            )

            if page is None:
                page = await context.new_page()
                await page.goto("https://cs2tracker.gg")

            input("Ensure CS2Tracker is ready, then press Enter...")

            while (
                get_num_of_messages(connection) < TARGET_MESSAGES
                and get_num_of_processed_players(connection) < MAX_PLAYERS
            ):
                processed = await process_next_player(connection, page)

                if not processed:
                    print("No more unprocessed players.")
                    break

                await asyncio.sleep(1)

            await browser.close()

    finally:
        connection.close()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
