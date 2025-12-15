from rest_framework import serializers
from .models import League, Team, Match, Event, Favorite

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "api_id", "name", "logo", "country"]

class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ["id", "api_id", "name", "country"]

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "type", "team", "player", "minute", "detail", "created_at"]

class MatchSerializer(serializers.ModelSerializer):
    home = TeamSerializer()
    away = TeamSerializer()
    league = LeagueSerializer()
    events = EventSerializer(many=True)
    class Meta:
        model = Match
        fields = ["id", "api_id", "league", "home", "away", "status", "minute", "kickoff", "home_score", "away_score", "events", "updated_at"]

class FavoriteSerializer(serializers.ModelSerializer):
    team = TeamSerializer()
    class Meta:
        model = Favorite
        fields = ["id", "user_identifier", "team", "created_at"]
