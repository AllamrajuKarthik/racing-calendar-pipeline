import os

# iCal feed URLs
FEEDS = {
    "WEC": "https://calendar.google.com/calendar/ical/61jccgg4rshh1temqk0dj4lens%40group.calendar.google.com/public/basic.ics",
    "WRC": "https://calendar.google.com/calendar/ical/fei68gpe16c85ed3jjdtvrn8ns%40group.calendar.google.com/public/basic.ics",
    "SRO_GT": "https://calendar.google.com/calendar/ical/kcelko7ictk6okcf4peougahlo%40group.calendar.google.com/public/basic.ics",
}

# Filtering

ALLOWED_CIRCUITS = ["Spa"]

# Telegram secrets (set these as environment variables, never hardcode them)
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Files
DB_FILE = "races.db"
LOG_FILE = "pipeline.log"
