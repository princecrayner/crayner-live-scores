from django.db import models

class League(models.Model):
    api_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.name

class Team(models.Model):
    api_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    logo = models.URLField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.name

class Match(models.Model):
    api_id = models.IntegerField(unique=True)
    league = models.ForeignKey(League, on_delete=models.SET_NULL, null=True, blank=True)
    home = models.ForeignKey(Team, related_name="home_matches", on_delete=models.SET_NULL, null=True)
    away = models.ForeignKey(Team, related_name="away_matches", on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    minute = models.IntegerField(null=True, blank=True)
    kickoff = models.DateTimeField(null=True, blank=True)
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.home} vs {self.away}"

class Event(models.Model):
    match = models.ForeignKey(Match, related_name="events", on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    team = models.CharField(max_length=10, blank=True, null=True)
    player = models.CharField(max_length=200, blank=True, null=True)
    minute = models.IntegerField(null=True, blank=True)
    detail = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Favorite(models.Model):
    user_identifier = models.CharField(max_length=200, default="anon")
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class DeviceToken(models.Model):
    token = models.CharField(max_length=512, unique=True)
    platform = models.CharField(max_length=50, default="expo")
    created_at = models.DateTimeField(auto_now_add=True)
