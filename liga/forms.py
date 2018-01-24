from django import forms


# action: post request to create_player
class JoinTournamentForm(forms.Form):
    tournament_name = ''
    hidden_tournament_id_field = forms.IntegerField(
        label="Pretend you've never seen this ;)",
        widget=forms.HiddenInput
    )

    def set_data(self, tournament):
        self.tournament_name = tournament.game_name
        self.fields['hidden_tournament_id_field'].initial = tournament.id
        return self


# action: post request to create_team/:tournament_id
class CreateTeamForm(forms.Form):
    team_name = forms.CharField(label='Team name')
    is_public = forms.BooleanField(label='Publicly visible')
    hidden_tournament_id_field = forms.IntegerField(
        label="Pretend you've never seen this ;)",
        widget=forms.HiddenInput
    )

    def set_data(self, tournament):
        self.fields['hidden_tournament_id_field'].initial = tournament.id
        return self


# action: post request to invite_player_to_team
class CreatePlayerInviteForm(forms.Form):
    player_name = ''

    hidden_team_id_field = forms.IntegerField(
        label="Pretend you've never seen this ;)",
        widget=forms.HiddenInput,
    )
    hidden_player_id_field = forms.IntegerField(
        label="Pretend you've never seen this ;)",
        widget=forms.HiddenInput,
    )

    def set_data(self, team, player):
        self.player_name = player.user.name  # TODO full_name
        self.fields['hidden_player_id_field'].initial = player.id
        self.fields['hidden_team_id_field'].initial = team.id
        return self


# action: post request to request_team
class CreateTeamRequestForm(forms.Form):
    team_name = ''

    hidden_team_id_field = forms.IntegerField(
        label="Pretend you've never seen this ;)",
        widget=forms.HiddenInput,
    )
    hidden_player_id_field = forms.IntegerField(
        label="Pretend you've never seen this ;)",
        widget=forms.HiddenInput,
    )

    def set_data(self, team, player):
        self.team_name = team.name
        self.fields['hidden_player_id_field'].initial = player.id
        self.fields['hidden_team_id_field'].initial = team.id
        return self


class AcceptPlayerInviteForm(forms.Form):
    team_name = ''

    hidden_invite_id_field = forms.IntegerField(
        label="Pretend you've never seen this ;)",
        widget=forms.HiddenInput,
    )

    def set_data(self, invite):
        self.team_name = invite.team.name  # TODO full_name
        self.fields['hidden_invite_id_field'].initial = invite.id
        return self


class AcceptTeamRequestForm(forms.Form):
    player_name = ''

    hidden_team_request_field = forms.IntegerField(
        label="Pretend you've never seen this ;)",
        widget=forms.HiddenInput,
    )

    def set_data(self, team_request):
        self.player_name = team_request.player.user.name  # TODO: full_name
        print(team_request.player, team_request.player.user.name)
        self.fields['hidden_team_request_field'].initial = team_request.id
        return self


# class CreateMatchForm(forms.Form):
#     # TODO
#
# class CreateScorePropositionForm(forms.Form):
#     # TODO
