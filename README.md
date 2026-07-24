# Racing Calendar Pipeline

An automation pipeline that tracks upcoming motorsport races (WEC, WRC, and
GT World Challenge's 24 Hours of Spa) and sends a Telegram alert whenever a
new race is added, a race's dates change, or a race is happening today.

## What it does

1. Fetches live iCal calendar feeds for three racing series
2. Filters out past races, test days, and qualifying sessions - keeping only
   real, upcoming races
3. Compares each race against a local SQLite database to detect what's new
   or changed since the last run
4. Sends a Telegram message for any new/changed race, and a separate alert
   on the morning of race day
5. Logs every step to a persistent log file
6. Runs automatically on a schedule via GitHub Actions - no server required

## Why these particular sources

- **WEC** and **WRC** - full season feeds, no filtering needed
- **GT World Challenge (SRO Intercontinental GT Challenge)** - this feed
  covers Bathurst, Nürburgring, Spa, and Indianapolis; filtered down to just
  the 24 Hours of Spa
- **F1** is intentionally excluded - Formula1.com already offers a native
  "subscribe to calendar" link, so there's no automation value in
  re-building something Google Calendar already does for free

## Architecture

```
config.py       - feed URLs, filter rules, secrets
fetcher.py      - downloads + parses iCal feeds into clean race data
database.py     - SQLite storage, detects new/changed races
notifier.py     - sends Telegram messages
logger.py       - sets up logging to file + terminal
main.py         - orchestrates the whole pipeline
```

Each file has exactly one job. `main.py` is the only file that knows about
all the others - everything else stays focused and independent.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Set your Telegram credentials as environment variables:

```bash
export TELEGRAM_BOT_TOKEN="your_token"
export TELEGRAM_CHAT_ID="your_chat_id"
```

Add your three feed URLs to `config.py`, then run:

```bash
python3 main.py
```

## Known limitations (V1)

- If a race's name changes mid-season (e.g. a sponsor change or a
  "Rescheduled" tag being added), the pipeline may treat it as a new race
  rather than an update, since matching is done by exact race name.
- The GT World Challenge filter matches on the word "Spa" appearing in the
  race name - a different or unusual naming format could be missed.

## Roadmap

- **V2**: sync races directly to Google Calendar, not just Telegram alerts
