import datetime
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
        self.player_name = player.user.full_name
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
        self.team_name = invite.team.full_name
        self.fields['hidden_invite_id_field'].initial = invite.id
        return self


class AcceptTeamRequestForm(forms.Form):
    player_name = ''

    hidden_team_request_field = forms.IntegerField(
        label="Pretend you've never seen this ;)",
        widget=forms.HiddenInput,
    )

    def set_data(self, team_request):
        self.player_name = team_request.player.user.full_name
        self.fields['hidden_team_request_field'].initial = team_request.id
        return self


class CreateMatchForm(forms.Form):
    opponent_name = ''

    inviting_team_id_hidden_field = forms.IntegerField(
        label="Pretend you've never seen this ;)",
        widget=forms.HiddenInput,
    )
    guest_team_id_hidden_field = forms.IntegerField(
        label="Pretend you've never seen this ;)",
        widget=forms.HiddenInput,
    )

    expires_at = forms.DateField(
        label="Expire after",
    )
    # TODO: Add default and widget !!!
    suggested_at = forms.DateField(
        label="Suggested match date",
    )
    # TODO: Add default and widget !!!

    def set_data(self, inviting_team, guest_team):
        self.opponent_name = guest_team.name
        self.fields['inviting_team_id_hidden_field'].initial = inviting_team.id
        self.fields['guest_team_id_hidden_field'].initial = guest_team.id
        return self


class CreateScorePropositionForm(forms.Form):
    hidden_match_id_field = forms.IntegerField(
        label="Pretend you've never seen this ;)",
        widget=forms.HiddenInput,
    )
    # TODO: Check if this is secure (see create_score_proposition view and data extraction from form fields)
    hidden_team_id_field = forms.IntegerField(
        label="Pretend you've never seen this ;)",
        widget=forms.HiddenInput,
    )
    my_score = forms.IntegerField(
        label="Inviting team score",
        widget=forms.NumberInput,
    )
    opponent_score = forms.IntegerField(
        label="Inviting team score",
        widget=forms.NumberInput,
    )

    def set_data(self, my_team, match):
        self.fields['hidden_match_id_field'].initial = match.id
        self.fields['hidden_team_id_field'].initial = my_team.id
        self.fields['my_score'].label = "{} score".format(my_team.name)
        self.fields['opponent_score'].label = "Opponent score"
        return self
