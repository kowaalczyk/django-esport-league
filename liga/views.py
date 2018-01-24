from datetime import datetime, date, timezone

from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from liga.forms import JoinTournamentForm, CreateTeamForm, CreatePlayerInviteForm, CreateTeamRequestForm, \
    AcceptPlayerInviteForm, AcceptTeamRequestForm, CreateMatchForm, CreateScorePropositionForm
from liga.models import Tournament, Team, TeamRequest, PlayerInvite, Match, Player, User
from liga import helpers


# Create your views here.

@login_required
def home(request):
    return render(request, 'liga/home.html')


# noinspection SpellCheckingInspection
@login_required
def index(request):
    us = request.user.social_auth.filter(provider='facebook')[0]
    fid = us.uid

    if not User.objects.filter(facebook_id=fid):
        helpers.fill_user_info(us)

    user = User.objects.get(facebook_id=fid)

    playable_tournaments = user.playable_tournaments.all()
    planned_tournaments = user.planned_tournaments.all()
    joinable_tournaments = user.joinable_tournaments.all()
    joinable_tournament_forms = [JoinTournamentForm().set_data(t) for t in joinable_tournaments]

    context = {
        'playable_tournaments': playable_tournaments,
        'planned tournaments': planned_tournaments,
        'joinable_tournament_forms': joinable_tournament_forms,
    }
    return render(request, 'liga/index.html', context)


@login_required
def tournament(request, tournament_id):
    fid = request.user.social_auth.filter(provider='facebook')[0].uid
    user_id = User.objects.get(facebook_id=fid)

    current_tournament = get_object_or_404(Tournament, id=tournament_id)
    print(current_tournament)
    player = get_object_or_404(Player, tournament_id=tournament_id, user_id=user_id)
    has_team = player.team is not None

    before_season = datetime.now(timezone.utc) < current_tournament.season_start

    if before_season:
        start_date = current_tournament.season_start
        if has_team:
            team_requests = TeamRequest.objects.filter(team=player.team).all()
            team_request_forms = [AcceptTeamRequestForm().set_data(tr) for tr in team_requests]

            free_players = current_tournament.players.filter(team__isnull=True).all()
            free_player_forms = [CreatePlayerInviteForm().set_data(player.team, fp) for fp in free_players]

            team_members = player.team.players.exclude(id=player.id).all()
            context = {
                'tournament': current_tournament,
                'has_team': has_team,
                'team': player.team,
                'team_players': team_members,
                'team_players_count': player.team.players.count(),
                'team_request_accept_forms': team_request_forms,
                'free_players_invite_forms': free_player_forms,
                'start_date': start_date,
            }
        else:
            public_teams = current_tournament.teams.filter(is_public=True).all()
            public_team_forms = [CreateTeamRequestForm().set_data(pt, player) for pt in public_teams]

            player_invites = PlayerInvite.objects.filter(player=player).all()
            player_invite_forms = [AcceptPlayerInviteForm().set_data(i) for i in player_invites]

            create_team_form = CreateTeamForm().set_data(current_tournament)
            context = {
                'tournament': current_tournament,
                'has_team': has_team,
                'create_team_form': create_team_form,
                'public_teams_request_forms': public_team_forms,
                'player_invite_forms': player_invite_forms,
            }
        return render(request, 'liga/tournament_before_season.html', context)

    else:
        # during season
        teams = current_tournament.teams.order_by('-score').all()
        context = {
            'tournament': current_tournament,
            'has_team': has_team,
            'player_team': player.team,
            'teams': teams,
        }
        return render(request, 'liga/tournament_during_season.html', context)


@login_required
def team(request, tournament_id, team_id):
    fid = request.user.social_auth.filter(provider='facebook')[0].uid
    user_id = User.objects.get(facebook_id=fid)

    current_tournament = get_object_or_404(Tournament, id=tournament_id)
    current_team = get_object_or_404(Team, id=team_id, tournament_id=tournament_id)
    player = get_object_or_404(Player, team=current_team, user=user)

    season_ended = current_tournament.season_end < datetime.now(timezone.utc)
    if season_ended:
        return redirect('tournaments', tournament_id=current_tournament.id)

    else:
        possible_opponents = current_team.possible_oponenets.all()
        possible_opponent_challenge_forms = [CreateMatchForm().set_data(current_team, opt)
                                             for opt in possible_opponents]

        planned_matches = current_team.planned_matches.all()
        played_matches = current_team.played_matches.order_by('-expires_at').all()

        print(possible_opponents.count())
        team_members = current_team.players.exclude(id=player.id).all()
        context = {
            'team': current_team,
            'tournament': current_tournament,
            'team_members': team_members,
            'planned_matches': planned_matches,
            'played_matches': played_matches,
            'possible_opponents_count': possible_opponents.count(),
            'possible_opponent_challenge_forms': possible_opponent_challenge_forms,
        }
        return render(request, 'liga/team.html', context)


@login_required
def match(request, tournament_id, match_id):
    fid = request.user.social_auth.filter(provider='facebook')[0].uid
    user_id = User.objects.get(facebook_id=fid)

    current_tournament = get_object_or_404(Tournament, id=tournament_id)
    current_match = get_object_or_404(Match, id=match_id)
    player = get_object_or_404(Player, tournament_id=tournament_id, user_id=user_id)
    current_team = player.team

    if current_team is None:
        return HttpResponseNotFound()

    if current_match.inviting_team != current_team and current_match.guest_team != current_team:
        return HttpResponseNotFound()

    expired = current_match.expires_at < datetime.now(timezone.utc).date()
    scored = current_match.guest_score is not None and current_match.inviting_score is not None
    won = not expired and scored and current_match.my_score(current_team) > current_match.opponent_score(current_team)

    opponent_score_proposition = current_match.opponent_score_proposition(current_team)
    my_score_proposition = current_match.my_score_proposition(current_team)
    if my_score_proposition is None and not expired:
        my_score_proposition_form = CreateScorePropositionForm().set_data(current_team, current_match)
    else:
        my_score_proposition_form = None

    context = {
        'tournament': current_tournament,
        'match': current_match,
        'opponent': current_match.other_team(current_team),
        'expired': expired,
        'scored': scored,
        'won': won,
        'my_score_proposition': my_score_proposition,
        'my_score_proposition_form': my_score_proposition_form,
        'opponent_score_proposition': opponent_score_proposition,
    }
    return render(request, 'liga/match.html', context)


@login_required
def create_player(request):
    fid = request.user.social_auth.filter(provider='facebook')[0].uid
    user_id = User.objects.get(facebook_id=fid)

    if request.method != 'POST':
        return HttpResponseNotFound()

    form = JoinTournamentForm(request.POST)
    if form.is_valid():
        player, created = Player.objects.get_or_create(
            tournament_id=form.cleaned_data['hidden_tournament_id_field'],
            user_id=user_id,
        )
        if created:
            print('CREATED:', player)
        else:
            print('WARNING:', 'unable to create new player')
        return redirect('tournament', tournament_id=player.tournament_id)

    else:
        # invalid form
        print('ERROR: form error')
        print(form.errors)
        return HttpResponseNotFound()


@login_required
def create_team(request, tournament_id):
    fid = request.user.social_auth.filter(provider='facebook')[0].uid
    user_id = User.objects.get(facebook_id=fid)

    if request.method != 'POST':
        return HttpResponseNotFound()

    player = get_object_or_404(Player, user_id=user_id, tournament_id=tournament_id)

    form = CreateTeamForm(request.POST)
    if form.is_valid():
        new_team, created = Team.objects.get_or_create(
            tournament_id=tournament_id,
            name=form.cleaned_data['team_name'],
            is_public=form.cleaned_data['is_public']
        )
        if created:
            print('CREATED:', new_team)
            player.team_id = new_team.id
            player.save()

            return redirect('tournament', tournament_id=player.tournament_id)
        else:
            print('WARNING:', 'unable to create new team')
            # TODO: Notify user about failure (probably team name was already used)
            return redirect('tournament', tournament_id=player.tournament_id)
    else:
        # invalid form
        print('ERROR: form error')
        print(form.errors)
        return redirect('tournament', tournament_id=tournament_id)


@login_required
def create_player_invite(request, tournament_id):
    fid = request.user.social_auth.filter(provider='facebook')[0].uid
    user_id = User.objects.get(facebook_id=fid)

    if request.method != 'POST':
        return HttpResponseNotFound()

    sending_player = get_object_or_404(Player, user_id=user_id, tournament_id=tournament_id)

    form = CreatePlayerInviteForm(request.POST)
    if form.is_valid():
        form_team_id = form.cleaned_data['hidden_team_id_field']

        if form_team_id != sending_player.team_id:
            return HttpResponseNotFound()

        current_team = get_object_or_404(Team, id=form_team_id)
        if current_team is None or current_team.tournament.season_start < datetime.now(timezone.utc):
            # no team or tournament already started
            return HttpResponseNotFound()

        invited_player = get_object_or_404(Player,
                                           id=form.cleaned_data['hidden_player_id_field'],
                                           tournament_id=current_team.tournament_id)
        if invited_player.team is not None:
            return HttpResponseNotFound()

        # assuming invites expire at the time of tournament start
        invite, created = PlayerInvite.objects.get_or_create(player=invited_player,
                                                             team=current_team,
                                                             expire_date=current_team.tournament.season_start.date())
        if created:
            print('CREATED:', invite)
            return redirect('tournament', tournament_id=tournament_id)
        else:
            print('WARNING:', 'unable to create new player invite')
            # TODO: Notify user about failure (invite already existed) -- or tournament started? check
            return redirect('tournament', tournament_id=tournament_id)

    else:
        # invalid form
        print('ERROR: form error')
        print(form.errors)
        return redirect('tournament', tournament_id=tournament_id)


@login_required
def create_team_requst(request, tournament_id):
    fid = request.user.social_auth.filter(provider='facebook')[0].uid
    user_id = User.objects.get(facebook_id=fid)

    if request.method != 'POST':
        return HttpResponseNotFound()

    sending_player = get_object_or_404(Player, user_id=user_id, tournament_id=tournament_id)

    form = CreateTeamRequestForm(request.POST)
    if form.is_valid():
        form_team_id = form.cleaned_data['hidden_team_id_field']
        form_team = get_object_or_404(Team, id=form_team_id, tournament_id=tournament_id, is_public=True)

        if form_team is None or form_team.tournament.season_start < datetime.now(timezone.utc):
            # no team or tournament already started
            return HttpResponseNotFound()

        # assuming team requests expire at the time of tournament start
        team_request, created = TeamRequest.objects.get_or_create(player=sending_player,
                                                                  team=form_team,
                                                                  expire_date=form_team.tournament.season_start.date())
        if created:
            print('CREATED:', team_request)
            return redirect('tournament', tournament_id=tournament_id)
        else:
            print('WARNING:', 'unable to create new team request')
            # TODO: Notify user about failure (invite already existed) -- or tournament started? check
            return redirect('tournament', tournament_id=tournament_id)

    else:
        # invalid form
        print('ERROR: form error')
        print(form.errors)
        return redirect('tournament', tournament_id=tournament_id)


@login_required
def accept_player_invite(request, tournament_id):
    fid = request.user.social_auth.filter(provider='facebook')[0].uid
    user_id = User.objects.get(facebook_id=fid)

    if request.method != 'POST':
        return HttpResponseNotFound()

    current_player = get_object_or_404(Player, tournament_id=tournament_id, user_id=user_id)

    form = AcceptPlayerInviteForm(request.POST)
    if form.is_valid():
        player_invite = get_object_or_404(PlayerInvite,
                                          id=form.cleaned_data['hidden_invite_id_field'],
                                          player_id=current_player.id)

        inviting_team = get_object_or_404(Team, id=player_invite.team_id, tournament_id=tournament_id)

        current_player.team = inviting_team
        current_player.save()
        player_invite.delete()

        return redirect('tournament', tournament_id=tournament_id)

    else:
        # invalid form
        print('ERROR: form error')
        print(form.errors)
        return redirect('tournament', tournament_id=tournament_id)

@login_required
def accept_team_request(request, tournament_id):
    fid = request.user.social_auth.filter(provider='facebook')[0].uid
    user_id = User.objects.get(facebook_id=fid)

    if request.method != 'POST':
        return HttpResponseNotFound()

    current_player = get_object_or_404(Player, tournament_id=tournament_id, user_id=user_id)

    form = AcceptTeamRequestForm(request.POST)
    if form.is_valid():
        team_request = get_object_or_404(TeamRequest,
                                         id=form.cleaned_data['hidden_team_request_field'],
                                         team=current_player.team)

        requesting_player = get_object_or_404(Player, id=team_request.player_id, tournament_id=tournament_id)

        requesting_player.team = current_player.team
        requesting_player.save()
        team_request.delete()

        return redirect('tournament', tournament_id=tournament_id)

    else:
        # invalid form
        print('ERROR: form error')
        print(form.errors)
        return redirect('tournament', tournament_id=tournament_id)

@login_required
def create_match(request, tournament_id):
    fid = request.user.social_auth.filter(provider='facebook')[0].uid
    user_id = User.objects.get(facebook_id=fid)
    if request.method != 'POST':
        return HttpResponseNotFound()

    current_player = get_object_or_404(Player, tournament_id=tournament_id, user_id=user_id)
    current_team = current_player.team
    if current_team is None:
        return HttpResponseNotFound()

    form = CreateMatchForm(request.POST)
    if form.is_valid():
        if form.cleaned_data['inviting_team_id_hidden_field'] != current_team.id:
            return HttpResponseNotFound()

        form_opponent = get_object_or_404(current_team.possible_oponenets,
                                          id=form.cleaned_data['guest_team_id_hidden_field'],
                                          tournament_id=tournament_id)

        current_match, created = Match.objects.get_or_create(
            inviting_team_id=current_team.id,
            guest_team_id=form_opponent.id,
            created_at=date.today(),
            suggested_at=form.cleaned_data['suggested_at'],
            expires_at=form.cleaned_data['expires_at'],
        )
        if not created:
            # match already existed TODO: Notify user
            return HttpResponseNotFound()

        print('CREATED:', current_match)
        return redirect('team', tournament_id=tournament_id, team_id=current_team.id)

    else:
        # invalid form TODO: Render errors
        print('ERROR: form error')
        print(form.errors)
        return redirect('team', tournament_id=tournament_id, team_id=current_team.id)

@login_required
def create_score_proposition(request, tournament_id, match_id):
    fid = request.user.social_auth.filter(provider='facebook')[0].uid
    user_id = User.objects.get(facebook_id=fid)
    if request.method != 'POST':
        return HttpResponseNotFound()

    current_player = get_object_or_404(Player, tournament_id=tournament_id, user_id=user_id)
    current_team = current_player.team
    if current_team is None:
        return HttpResponseNotFound()

    current_match = get_object_or_404(Match,
                                      id=match_id,
                                      inviting_team__tournament_id=tournament_id,
                                      guest_team__tournament_id=tournament_id)
    if current_team != current_match.inviting_team and current_team != current_match.guest_team:
        return HttpResponseNotFound()

    form = CreateScorePropositionForm(request.POST)
    if form.is_valid():
        updated = current_match.update_proposition(current_team,
                                                   form.cleaned_data['my_score'],
                                                   form.cleaned_data['opponent_score'])
        if updated:
            print('UPDATE score_proposition:', current_match)
            return redirect('match', tournament_id=tournament_id, match_id=match_id)

        else:
            print('WARNING: match score propositions not updated!')
            # TODO: Render errors
            return redirect('match', tournament_id=tournament_id, match_id=match_id)

    else:
        # invalid form TODO: Render errors
        print('ERROR: form error')
        print(form.errors)
        return redirect('match', tournament_id=tournament_id, match_id=match_id)

# TODO actions (handling POST request):
# log in
# log out (user)
