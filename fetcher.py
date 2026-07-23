#This file converts the URLs into actual usable data
from datetime import date

import requests
from icalendar import Calendar

# As we are only focussed on race session not the qualifying or other events.
EXCLUDE_KEYWORDS = ["test", "qual", "prologue"]


def fetch_races(url, series_name):

    #Download the iCal feed at `url` and return every event in it as a list
    #of dicts, e.g. {"series": "WEC", "name": "6 Hours of Imola", "start_date": "2026-04-17", "end_date": "2026-04-19"}

    response = requests.get(url)
    response.raise_for_status()

    calendar = Calendar.from_ical(response.text)

    races = []
    for component in calendar.walk():
        if component.name != "VEVENT":
            continue

        race = {
            "series": series_name,
            "name": str(component.get("summary")),
            "start_date": component.get("dtstart").dt.isoformat(),
            "end_date": component.get("dtend").dt.isoformat(),
        }
        races.append(race)

    return races


def filter_upcoming_races(races):
   #We only want the races that are yet to happen. So here we are filtering that. We don't already happened races
    today = date.today().isoformat()

    result = []
    for race in races:
        if race["start_date"] < today:
            continue
        if any(word in race["name"].lower() for word in EXCLUDE_KEYWORDS):
            continue
        result.append(race)

    return result


def filter_by_circuit(races, allowed_circuits):
    # This is optional- but my priority. This keeps only races whose name mentions one of the allowed circuits.
    return [race for race in races if any(circuit in race["name"] for circuit in allowed_circuits)]
