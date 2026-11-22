
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
    get_num_of_messages
)

async def process_next_player(connection: sqlite3.Connection, page):
    steamid64 = get_next_unprocessed_player(connection)

    if steamid64 is None:
        print("No unprocessed players.")
        return

    print(f"Processing player: {steamid64}")

    try:
        data = await fetch_player_matches(page, steamid64)

        messages = parse_api_messages(data)

        ingest_messages(messages, connection)

        mark_player_as_processed(steamid64, connection)

        connection.commit()

        print(f"Fetched {len(messages)} messages.")
        print(f"Discovered {len(data['matches'])} matches.")
        print("Total players:", get_num_of_players(connection))
        print("Processed players:", get_num_of_processed_players(connection))
        print("Total messages:", get_num_of_messages(connection))

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

            await process_next_player(connection, page)

            await browser.close()

    finally:
        connection.close()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
