from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tournament/<int:tournament_id>/', views.tournament, name='tournament'),
    path('tournament/<int:tournament_id>/teams/<int:team_id>', views.tournament, name='team'),
    path('create-player/', views.create_player, name='join-tournament'),
    path('create-team/<int:tournament_id>/', views.create_team, name='create-team'),
]
