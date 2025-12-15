from django.core.management.base import BaseCommand
from api.services.fetcher import fetch_live_fixtures, fetch_fixture_events
from api.models import League, Team, Match, Event
from datetime import datetime

class Command(BaseCommand):
    help = "Fetch live fixtures from API-Football and sync into DB"

    def handle(self, *args, **options):
        try:
            fixtures = fetch_live_fixtures()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Fetch error: {e}"))
            return

        self.stdout.write(f"Fetched {len(fixtures)} fixtures")
        for item in fixtures:
            fixture = item.get("fixture", {})
            teams = item.get("teams", {})
            league_info = item.get("league", {})
            goals = item.get("goals", {})

            # league
            league, _ = League.objects.get_or_create(api_id=league_info.get("id") or 0, defaults={
                "name": league_info.get("name") or "",
                "country": league_info.get("country") or ""
            })

            # teams
            home_info = teams.get("home") or {}
            away_info = teams.get("away") or {}
            home, _ = Team.objects.get_or_create(api_id=home_info.get("id") or 0, defaults={
                "name": home_info.get("name") or "",
                "logo": home_info.get("logo") or "",
                "country": home_info.get("country") or ""
            })
            away, _ = Team.objects.get_or_create(api_id=away_info.get("id") or 0, defaults={
                "name": away_info.get("name") or "",
                "logo": away_info.get("logo") or "",
                "country": away_info.get("country") or ""
            })

            kickoff = fixture.get("date")
            kickoff_dt = None
            if kickoff:
                try:
                    kickoff_dt = datetime.fromisoformat(kickoff.replace("Z", "+00:00"))
                except:
                    kickoff_dt = None

            match, created = Match.objects.update_or_create(
                api_id=fixture.get("id"),
                defaults={
                    "league": league,
                    "home": home,
                    "away": away,
                    "status": fixture.get("status", {}).get("short") or fixture.get("status", {}).get("long"),
                    "minute": fixture.get("status", {}).get("elapsed"),
                    "kickoff": kickoff_dt,
                    "home_score": goals.get("home") or 0,
                    "away_score": goals.get("away") or 0
                }
            )

            # events
            try:
                evs = fetch_fixture_events(fixture.get("id"))
                # clear and recreate (simple)
                Event.objects.filter(match=match).delete()
                for e in evs:
                    Event.objects.create(
                        match=match,
                        type=e.get("type"),
                        team=("home" if e.get("team", {}).get("id") == home.api_id else "away"),
                        player=e.get("player", {}).get("name"),
                        minute=e.get("time", {}).get("elapsed"),
                        detail=e.get("detail")
                    )
            except Exception as ee:
                self.stdout.write(self.style.WARNING(f"Events fetch failed for {fixture.get('id')}: {ee}"))

        self.stdout.write(self.style.SUCCESS("Sync complete."))
