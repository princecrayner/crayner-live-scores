import requests
from django.conf import settings
from datetime import datetime

API_URL = "https://v3.football.api-sports.io"

HEADERS = {"x-apisports-key": settings.API_FOOTBALL_KEY}

def fetch_live_fixtures():
    """Return the 'response' payload from API-Football for live fixtures."""
    url = f"{API_URL}/fixtures"
    params = {"live": "all"}
    r = requests.get(url, headers=HEADERS, params=params, timeout=15)
    r.raise_for_status()
    return r.json().get("response", [])

def fetch_fixture_events(fixture_id):
    url = f"{API_URL}/fixtures/events"
    params = {"fixture": fixture_id}
    r = requests.get(url, headers=HEADERS, params=params, timeout=10)
    r.raise_for_status()
    return r.json().get("response", [])
