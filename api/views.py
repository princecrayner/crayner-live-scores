from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from .models import Match, Team
from .serializers import MatchSerializer
from .services.fetcher import fetch_live_fixtures

class MatchListView(generics.ListAPIView):
    queryset = Match.objects.select_related('home','away','league').prefetch_related('events').all().order_by('-kickoff')
    serializer_class = MatchSerializer

class MatchDetailView(generics.RetrieveAPIView):
    queryset = Match.objects.select_related('home','away','league').prefetch_related('events').all()
    serializer_class = MatchSerializer
    lookup_field = 'api_id'

# frontend view
def live_page(request):
    return render(request, "live.html")

# quick endpoint to call remote API directly (optional)
@api_view(['GET'])
def live_remote(request):
    try:
        data = fetch_live_fixtures()
        return Response({"success": True, "data": data})
    except Exception as e:
        return Response({"success": False, "error": str(e)})
