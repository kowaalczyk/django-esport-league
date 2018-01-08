from datetime import datetime, date

from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404

# Create your views here.
from liga.models import Tournament, Team, TeamRequest, PlayerInvite, Match


def index(request):
    # TODO: require sign in user
    tournament_list = Tournament.objects.all()
    # TODO: split to tournaments whre user is a player and joinable tournaments
    context = {
        'tournament_list': tournament_list,
    }
    return render(request, 'index.html', context)


def tournament(request, tournament_id):
    user = 0  # TODO: get from session
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    player = get_object_or_404(tournament.player_set, user=user)
    before_season = tournament.season_end < datetime.now() or tournament.season_start > datetime.now()

    if before_season:
        has_team = player.team is not None
        if has_team:
            team_requests = TeamRequest.objects.filter(team=player.team)
            free_players = tournament.player_set.filter(team=None)
            context = {
                'has_team': has_team,
                'team': player.team,
                'team_requests': team_requests,
                'free_players': free_players
            }
        else:
            public_teams = tournament.team_set.filter(is_public=True)
            player_invites = PlayerInvite.objects.filter(player=player)
            context = {
                'has_team': has_team,
                'public_teams': public_teams,
                'player_invites': player_invites
            }
        return render(request, 'tournament_before_season.html', context)

    else:
        team = get_object_or_404(player.team)
        score = 0  # TODO: # of teams 2x select count for score is too much, add score field to the team
        other_teams = tournament.team_set.exclude(team=team)  # TODO: order_by score
        context = {
            'team': team,
            'other_teams': other_teams
        }
        return render(request, 'tournament_during_season.html', context)


def team(request, team_id):
    user = 0  # TODO: get from session
    team = get_object_or_404(Team, pk=team_id)
    player = get_object_or_404(team.player_set, user=user)
    tournament = get_object_or_404(team.tournament)
    before_season = tournament.season_end < datetime.now() or tournament.season_start > datetime.now()

    if before_season:
        pending_matches = None
        played_matches = None
        possible_opponents = None
    else:
        # TODO: This is way too complex, move queries to model and simplify (raw sql?)
        pending_inviting_matches = team.inviting_matches.filter(expires_at__lte=date.today())
        pendding_guest_matches = team.guest_matches.filter(expires_at__lte=date.today())
        pending_matches = pending_inviting_matches | pendding_guest_matches
        played_inviting_matches = team.inviting_matches.filter(expires_at__gt=date.today())
        played_quest_matches = team.guest_matches.filter(expires_at__gt=date.today())
        played_matches = played_inviting_matches | played_quest_matches
        # TODO: Delete all matches after season is finished, or filter match dates here
        possible_opponents = tournament.team_set.exclude(pk__in=played_matches)

    context = {
        'before_season': before_season,
        'team_members': team.player_set,
        'pending_matches': pending_matches,
        'match_history': played_matches,
        'possible_opponents': possible_opponents
    }
    return render(request, 'team.html', context)


def match(request, match_id):
    user = 0  # TODO: get from session
    match = get_object_or_404(Match, pk=match_id)
    player = match.inviting_team.player_set.filter(user=user) | match.guest_team.player_set.filter(user=user)
    if player.count() == 0:
        return HttpResponseNotFound()  # TODO: Not sure if get_or_404 works with quryse unions so I left this
    context = {
        'match': match
    }
    return render(request, 'match.html', context)

# TODO actions (handling POST request):
# log in
# log out (user)
# create tournament (user) -- django admin
# create season (tournament, user) -- django admin
# delete tournament (tournament, user) -- django admin
# create player (tournament, user)
# delete player (tournament, player, user) -- django admin
# create team (tournament, user)
# update team (tournament, team, user)
# delete team (tournament, team, user) -- django admin
# invite to team (tournament, team, player, user)
# request team (tournament, team, player, user)
# reject player invitation (tournament, team, player, user, playerinvite)
# accept player invitation (tournament, team, player, user, playerinvite)
# accept team request (tournament, team, player, user, teamrequest)
# reject team request (tournament, team, player, user, teamrequest)
# create match (tournament, team, opponent team, user)
# create score proposition (tournament, match, user)
