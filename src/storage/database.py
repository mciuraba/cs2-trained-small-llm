import sqlite3
from sqlite3 import Connection

def create_database():
    connection = sqlite3.connect("data/cs2.db")

    cursor = connection.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS players(steamid64 TEXT PRIMARY KEY, has_been_processed INTEGER NOT NULL DEFAULT 0)"
    )

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages(
            steamid64 TEXT,
            name TEXT NOT NULL,
            text TEXT NOT NULL,
            team TEXT,
            round INTEGER NOT NULL,
            seq INTEGER,
            played_at TEXT,
            share_code TEXT,
            map TEXT,

            PRIMARY KEY (share_code, seq)
        )
    """
    )

    connection.commit()

    connection.close()


def add_player(steamid64: str, connection: Connection):
    cur = connection.cursor()

    cur.execute(
        "INSERT OR IGNORE INTO players (steamid64) VALUES (?)",
        (steamid64,)
    )

    #connection.commit()

def add_message(message: dict, connection: Connection):
    '''
    Takes message dicitonary (single message) and puts it into cs2.db using connection from argument.
    '''

    cur = connection.cursor()

    cur.execute("""
        INSERT OR IGNORE INTO messages(
            steamid64, name, text, team, round, seq, played_at, share_code, map
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        ,(
            message["steamid64"],
            message["name"],
            message["text"],
            message["team"],
            message["round"],
            message["seq"],
            message["played_at"],
            message["share_code"],
            message["map"]
        )
    )

def get_messages_from_steamid(steamid64: str, connection: Connection):
    cur = connection.cursor()

    cur.execute(
        "SELECT text FROM messages WHERE steamid64 = ?",
        (steamid64,)
    )

    return [row[0] for row in cur.fetchall()]

def get_all_steamids(connection: Connection) -> list:
    """
    Retrieves all of unique steamid64 from messages table from cs2.db
    """

    cur = connection.cursor()

    cur.execute(
        "SELECT steamid64 FROM players"
    )

    return [row[0] for row in cur.fetchall()]

def get_num_of_messages(connection: Connection) -> int:
    cur = connection.cursor()

    cur.execute(
        "SELECT COUNT(*) FROM messages"
    )

    return cur.fetchone()[0]

def get_messages_in_order(connection: Connection):
    """
    Returns messages from a match in order, ordered by sequence that they appeared in.
    """

    # for each share_code (match), in order to sequence

    # get all share_code -> so each match

    cur = connection.cursor()

    cur.execute(
        "SELECT DISTINCT share_code FROM messages GROUP BY share_code ORDER BY MIN(played_at) ASC"
    )
    share_codes = [row[0] for row in cur.fetchall()]
    matches = []

    for code in share_codes:
        cur.execute(
            "SELECT seq, steamid64, text, team, round FROM messages WHERE share_code = ? ORDER BY seq ASC",
            (code,)
        )
        messages = cur.fetchall()

        matches.append({
            "share_code": code,
            "messages": [
                {
                    "seq": seq,
                    "steamid64":steamid64,
                    "text":text,
                    "team": team,
                    "round":round
                }
                for seq, steamid64, text, team, round in messages
            ]
        })

    return matches

def ingest_messages(messages: list[dict], connection: Connection):
    '''
    Puts all of messages in database from a list of dictionaries, accordingly (players and messages table).
    '''
    for message in messages:
        add_message(message, connection)
        # conditional for add_player (only if current database has less than 500 )
        add_player(message["steamid64"], connection)


def get_next_unprocessed_player(connection: Connection) -> str | None:
    '''
    Selects next unprocessed player from the database.
    Returns next unprocessed player's steamid64
    '''

    cur = connection.cursor()

    cur.execute(
        "SELECT steamid64 FROM players WHERE has_been_processed = 0 ORDER BY steamid64 LIMIT 1"
    )
    res = cur.fetchone()

    return res[0] if res else None



def mark_player_as_processed(steamid64: str, connection: Connection):
    cur = connection.cursor()
    cur.execute(
        "UPDATE players SET has_been_processed = 1 WHERE steamid64 = ?",
        (steamid64,)
    )

def get_num_of_players(connection: Connection) -> int:
    cur = connection.cursor()
    cur.execute("SELECT COUNT(*) FROM players")
    return cur.fetchone()[0]


def get_num_of_processed_players(connection: Connection) -> int:
    cur = connection.cursor()
    cur.execute("""
        SELECT COUNT(*)
        FROM players
        WHERE has_been_processed = 1
    """)
    return cur.fetchone()[0]

def remove_spam_messages(connection: Connection, threshold: int = 7):
    cur = connection.cursor()

    cur.execute("""
        DELETE from messages
        WHERE (share_code, steamid64, LOWER(TRIM(text))) IN (
            SELECT share_code, steamid64, LOWER(TRIM(text))
            FROM messages
            GROUP BY share_code, steamid64, LOWER(TRIM(text))
            HAVING COUNT(*) > ?
        )

    """, (threshold, ))

    deleted = cur.rowcount

    return deleted
