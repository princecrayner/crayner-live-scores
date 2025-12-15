from django.contrib import admin
from .models import League, Team, Match, Event, Favorite, DeviceToken

admin.site.register(League)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Event)
admin.site.register(Favorite)
admin.site.register(DeviceToken)
