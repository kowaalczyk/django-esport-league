from django.urls import path

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    #url(r'^$', views.home, name='home'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    path('', views.index, name='index'),
    path('tournament/<int:tournament_id>/',
         views.tournament,
         name='tournament'),
    path('tournament/join',
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
