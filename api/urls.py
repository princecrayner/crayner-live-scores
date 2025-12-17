from django.urls import path
from . import views

urlpatterns = [
    path('matches/', views.MatchListView.as_view(), name='matches'),
    path('match/<int:api_id>/', views.MatchDetailView.as_view(), name='match-detail'),
    path('live-remote/', views.live_remote, name='live-remote'),
    path('livepage/', views.live_page, name='live-page'),
    path('trigger-fetch/', views.trigger_fetch, name='trigger-fetch'),
]

