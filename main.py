"""
The main.py file. This does the following tasks

  1. Fetch races from all three feeds
  2. Filter down to upcoming real races
  3. Compare each race against what's already in the database
  4. If new or changed: save to DB + send a Telegram message
  5. Log every step along the way
"""

from config import FEEDS, ALLOWED_CIRCUITS
from fetcher import fetch_races, filter_upcoming_races, filter_by_circuit
from database import setup_database, get_connection, find_existing_race, save_new_race, update_race
from notifier import send_telegram_message
from logger import get_logger

logger = get_logger()


def process_feed(series_name, url, conn):
    logger.info(f"Fetching {series_name}")
    races = fetch_races(url, series_name)
    races = filter_upcoming_races(races)

    if series_name == "SRO_GT":
        races = filter_by_circuit(races, ALLOWED_CIRCUITS)

    logger.info(f"{series_name}: {len(races)} upcoming races found")

    for race in races:
        existing = find_existing_race(conn, race["series"], race["name"])

        if existing is None:
            save_new_race(conn, race)
            message = f"New race: {race['series']} - {race['name']} on {race['start_date'][:10]}"
            send_telegram_message(message)
            logger.info(f"NEW -> notified Telegram: {race['name']}")
            continue

        race_id, old_start, old_end = existing
        if old_start != race["start_date"] or old_end != race["end_date"]:
            update_race(conn, race_id, race)
            message = f"Race updated: {race['series']} - {race['name']} is now on {race['start_date'][:10]}"
            send_telegram_message(message)
            logger.info(f"UPDATED -> notified Telegram: {race['name']}")
        else:
            logger.info(f"no change: {race['name']}")


def run_pipeline():
    logger.info("=== Pipeline run started ===")
    setup_database()
    conn = get_connection()

    for series_name, url in FEEDS.items():
        process_feed(series_name, url, conn)

    conn.close()
    logger.info("=== Pipeline run finished ===")


if __name__ == "__main__":
    run_pipeline()
