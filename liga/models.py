from datetime import datetime

from django.db import models



class Faculty(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class User(models.Model):
    facebook_id = models.IntegerField()
    name = models.CharField(max_length=60)
    surname = models.CharField(max_length=60)
    mail = models.CharField(max_length=60)

    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="users")

    def __str__(self):
        return self.name

    @property
    def playable_tournaments(self):
        return Tournament.get_ongoing_tournaments().filter(players__user=self)

    @property
    def joinable_tournaments(self):
        return Tournament.get_planed_tournaments().exclude(players__user=self)


class Tournament(models.Model):
    game_name = models.CharField(max_length=60)
    season_start = models.DateTimeField()
    season_end = models.DateTimeField()
    team_size = models.IntegerField()

    def __str__(self):
        return self.game_name

    @staticmethod
    def get_ongoing_tournaments():
        return Tournament.objects.filter(season_start__lt=datetime.now(), season_end__gt=datetime.now())

    @staticmethod
    def get_planed_tournaments():
        return Tournament.objects.filter(season_start__gt=datetime.now())


class Team(models.Model):
    name = models.CharField(max_length=120)
    is_public = models.BooleanField(default=True)

    tournament = models.ForeignKey(Tournament,
                                   on_delete=models.CASCADE,
                                   related_name="teams")

    @property #pozwala na używanie jako pola
    def matches(self):
        return Match.objects.filter(inviting_team=self) | Match.objects.filter(guest_team=self)

    def possible_oponenets(self):
        return Team.objects.filter(tournament=self.tournament)\
            .exclude(inviting_matches__in=self.matches)\
            .exclude(guest_matches__in=self.matches)\
            .exclude(pk=self.pk)

    def __str__(self):
        return self.name


class Player(models.Model):
    tournament = models.ForeignKey(Tournament,
                                   on_delete=models.CASCADE,
                                   related_name="players")
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="players")
    team = models.ForeignKey(Team,
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True,
                             related_name="players")

    def __str__(self):
        return "{} in {}".format(self.user.name, self.tournament.game_name)


class Match(models.Model):
    created_at = models.DateField()
    expires_at = models.DateField()
    suggested_at = models.DateField(null=True, blank=True)
    inviting_score = models.IntegerField(null=True, blank=True)
    guest_score = models.IntegerField(null=True, blank=True)

    inviting_team = models.ForeignKey(Team,
                                      on_delete=models.CASCADE,
                                      related_name='inviting_matches')
    guest_team = models.ForeignKey(Team,
                                   on_delete=models.CASCADE,
                                   related_name='guest_matches')

    def __str__(self):
        return "{} vs. {}".format(self.inviting_team.name, self.guest_team.name)


class ScoreProposition(models.Model):
    inviting_score = models.IntegerField(null=True, blank=True)
    guest_score = models.IntegerField(null=True, blank=True)

    suggesting_team = models.ForeignKey(Team,
                                        on_delete=models.CASCADE)
    match = models.ForeignKey(Match,
                              on_delete=models.CASCADE)


class PlayerInvite(models.Model):
    expire_date = models.DateField()

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)


class TeamRequest(models.Model):
    expire_date = models.DateField()

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
