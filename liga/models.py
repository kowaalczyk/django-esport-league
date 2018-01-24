from datetime import datetime

from django.db import models
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce


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
    def full_name(self):
        return self.name + ' ' + self.surname

    @property
    def playable_tournaments(self):
        return Tournament.get_ongoing_tournaments().filter(players__user=self)

    @property
    def joinable_tournaments(self):
        return Tournament.get_planed_tournaments().exclude(players__user=self)

    @property
    def planned_tournaments(self):
        return Tournament.get_planed_tournaments().filter(players__user=self)


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
    score = models.IntegerField(default=0)

    @property
    def matches(self):
        return Match.objects.filter(inviting_team=self) | Match.objects.filter(guest_team=self)

    @property
    def played_matches(self):
        return self.matches.exclude(inviting_score__isnull=True).exclude(guest_score__isnull=True)

    @property
    def planned_matches(self):
        return self.matches.filter(inviting_score__isnull=True).filter(guest_score__isnull=True)

    @property
    def possible_oponenets(self):
        return Team.objects.filter(tournament=self.tournament) \
            .exclude(inviting_matches__in=self.matches) \
            .exclude(guest_matches__in=self.matches) \
            .exclude(pk=self.pk)

    @property
    def ranking(self):
        return Team.objects.filter(score__gt=self.score).aggregate(ranking=Count('score'))['ranking'] + 1

    def update_score(self):
        self.score = self.inviting_matches.aggregate(sum=Coalesce(Sum('inviting_score'), 0))['sum'] + \
                     self.guest_matches.aggregate(sum=Coalesce(Sum('guest_score'), 0))['sum']
        self.save()

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


class ScoreProposition(models.Model):
    inviting_score = models.IntegerField(null=True, blank=True)
    guest_score = models.IntegerField(null=True, blank=True)

    suggesting_team = models.ForeignKey(Team,
                                        on_delete=models.CASCADE)


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

    host_proposition = models.OneToOneField(ScoreProposition,
                                            null=True,
                                            blank=True,
                                            on_delete=models.SET_NULL,
                                            related_name='match_h')

    guest_proposition = models.OneToOneField(ScoreProposition,
                                             null=True,
                                             blank=True,
                                             on_delete=models.SET_NULL,
                                             related_name='match_g')

    def other_team(self, my_team):
        if my_team == self.inviting_team:
            return self.guest_team
        else:
            return self.inviting_team

    def my_score_proposition(self, my_team):
        if my_team == self.inviting_team:
            return self.host_proposition
        else:
            return self.guest_proposition

    def opponent_score_proposition(self, my_team):
        if my_team == self.inviting_team:
            return self.guest_proposition
        else:
            return self.host_proposition

    def my_score(self, my_team):
        if my_team == self.inviting_team:
            return self.inviting_score
        else:
            return self.guest_score

    def opponent_score(self, my_team):
        if my_team == self.inviting_team:
            return self.guest_score
        else:
            return self.inviting_score

    def update_proposition(self, team, my_score, opponent_score):
        if team == self.inviting_team:
            if self.host_proposition is not None:
                self.host_proposition.inviting_score = my_score
                self.host_proposition.guest_score = opponent_score
            else:
                self.host_proposition = ScoreProposition(inviting_score=my_score,
                                                         guest_score=opponent_score,
                                                         suggesting_team=team)
                self.host_proposition.save()

        elif team == self.guest_team:
            if self.guest_proposition is not None:
                self.guest_proposition.inviting_score = opponent_score
                self.guest_proposition.guest_score = my_score
            else:
                self.guest_proposition = ScoreProposition(inviting_score=opponent_score,
                                                          guest_score=my_score,
                                                          suggesting_team=team)
                self.guest_proposition.save()

        else:
            return False

        gg = self.guest_proposition.guest_score
        hg = self.host_proposition.guest_score
        gh = self.guest_proposition.inviting_score
        hh = self.host_proposition.inviting_score

        if gg == hg and gh == hh:  # checking if propositions matching
            self.inviting_score = gh
            self.guest_score = gg

        self.save()

        self.inviting_team.update_score()
        self.guest_team.update_score()

        return True

    def __str__(self):
        return "{} vs. {}".format(self.inviting_team.name, self.guest_team.name)


class PlayerInvite(models.Model):
    expire_date = models.DateField()

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)


class TeamRequest(models.Model):
    expire_date = models.DateField()

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
