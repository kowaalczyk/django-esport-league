from django import forms

class JoinTournamentForm(forms.Form):


class CreateTeamForm(forms.Form):
    # TODO

class UpdateTeamForm(forms.Form):
    # TODO

class InviteToTeamForm(forms.Form):
    # TODO

class RequestTeamForm(forms.Form):
    # TODO

# https://docs.djangoproject.com/en/2.0/ref/forms/api/#dynamic-initial-values
class ManagePlayerInviteForm(forms.Form):
    accept_invite_field = forms.TypedChoiceField(
        empty_value=False,
        label='DATA NOT SET !!!',
        coerce=lambda x: x == 'True',
        choices=((False, 'No'), (True, 'Yes')),
        widget=forms.RadioSelect
    )

    def set_data(self, team_name, player_invite_id):
        self.accept_invite_field.label = "Do You want to join {}?".format(team_name)
        # TODO: Finish from here


class ManageTeamRequestForm(forms.Form):
    # TODO

class CreateMatchForm(forms.Form):
    # TODO

class CreateScorePropositionForm(forms.Form):
    # TODO
