import sqlite3
from sqlite3 import Connection

def create_database():
    connection = sqlite3.connect("data/cs2.db")

    cursor = connection.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS players(steamid64 TEXT PRIMARY KEY)"
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
        "SELECT DISTINCT steamid64 FROM messages"
    )

    return [row[0] for row in cur.fetchall()]

def get_num_of_messages(connection: Connection) -> int:
    n_of_mess = 0

    cur = connection.cursor()

    cur.execute(
        "SELECT COUNT(*) FROM messages"
    )
    n_of_mess = cur.fetchall()

    return n_of_mess[0][0]


    
