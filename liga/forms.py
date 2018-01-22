from django import forms


# Form rendered for each joinable tournament on index page
# TODO: This should only show submit button - check before creating other forms
# action: post request to create_player
class JoinTournamentForm(forms.Form):
    hidden_tournament_id_field = forms.IntegerField(
        label='THIS SHOULD BE HIDDEN !!!',
        widget=forms.HiddenInput
    )

    def set_data(self, team_id):
        self.hidden_tournament_id_field.coerce = lambda x: team_id
        self.hidden_tournament_id_field.empty_value = team_id
        self.hidden_tournament_id_field.choices = (team_id, team_id)

#
# # action: post request to create_team/:tournament_id
# class CreateTeamForm(forms.Form):
#     # TODO
#
# # action: post request to update_team
# class UpdateTeamForm(forms.Form):
#     # TODO
#
# # action: post request to invite_player_to_team
# class InviteToTeamForm(forms.Form):
#     # TODO
#
# # action: post request to request_team
# class RequestTeamForm(forms.Form):
#     # TODO
#
# # https://docs.djangoproject.com/en/2.0/ref/forms/api/#dynamic-initial-values
# class ManagePlayerInviteForm(forms.Form):
#     accept_invite_field = forms.TypedChoiceField(
#         empty_value=False,
#         label='DATA NOT SET !!!',
#         coerce=lambda x: x == 'True',
#         choices=((False, 'No'), (True, 'Yes')),
#         widget=forms.RadioSelect
#     )
#
#     def set_data(self, team_name):
#         self.accept_invite_field.label = "Do You want to join {}?".format(team_name)
#
#
# class ManageTeamRequestForm(forms.Form):
#     accept_request_field = forms.TypedChoiceField(
#         empty_value=False,
#         label='DATA NOT SET !!!',
#         coerce=lambda x: x == 'True',
#         choices=((False, 'No'), (True, 'Yes')),
#         widget=forms.RadioSelect
#     )
#
#     def set_data(self, player_name):
#         self.accept_invite_field.label = "Do You want to add {} to Your team?".format(player_name)
#
# class CreateMatchForm(forms.Form):
#     # TODO
#
# class CreateScorePropositionForm(forms.Form):
#     # TODO
