from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tournament/<int:tournament_id>/', views.tournament, name='tournament')
]
