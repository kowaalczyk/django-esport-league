from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('tournament/<int:tournament_id>/',
         views.tournament,
         name='tournament'),
    path('tournament/<int:tournament_id>/players/create/',
         views.create_player,
         name='join-tournament'),
    path('tournament/<int:tournament_id>/teams/<int:team_id>/',
         views.team,
         name='team'),
    path('tournament/<int:tournament_id>/teams/create/',
         views.create_team,
         name='create-team'),
    path('tournament/<int:tournament_id>/invites/create/',
         views.create_player_invite,
         name='create-player-invite'),
    path('tournament/<int:tournament_id>/requests/create/',
         views.create_team_requst,
         name='create-team-request'),
    path('tournament/<int:tournament_id>/matches/<int:match_id>/',
         views.match,
         name='match'),
]

