import sqlite3
from config import DB_FILE


def get_connection():
    return sqlite3.connect(DB_FILE)


def setup_database():
    #Create the races table if it doesn't already exist. Can to run every time.
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS races (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            series TEXT,
            name TEXT,
            start_date TEXT,
            end_date TEXT
        )
    """)
    conn.commit()
    conn.close()


def find_existing_race(conn, series, name):
    #Look for a race that's already stored, matched by series + name.
    cursor = conn.execute(
        "SELECT id, start_date, end_date FROM races WHERE series = ? AND name = ?",
        (series, name),
    )
    return cursor.fetchone()


def save_new_race(conn, race):
    #Insert a race we've never seen before.
    conn.execute(
        "INSERT INTO races (series, name, start_date, end_date) VALUES (?, ?, ?, ?)",
        (race["series"], race["name"], race["start_date"], race["end_date"]),
    )
    conn.commit()


def update_race(conn, race_id, race):
    #Update a race whose dates have changed since last time.
    conn.execute(
        "UPDATE races SET start_date = ?, end_date = ? WHERE id = ?",
        (race["start_date"], race["end_date"], race_id),
    )
    conn.commit()


def get_all_races(conn):
    #Return every race we've stored - this is to check if there's a race happening today.
    cursor = conn.execute("SELECT series, name, start_date, end_date FROM races")
    return cursor.fetchall()