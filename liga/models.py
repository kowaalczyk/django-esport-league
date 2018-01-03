from django.db import models

# Create your models here.


class Faculty(models.Model):
    name=models.CharField(max_length=60)


class User(models.Model):
    facebook_id=models.IntegerField()
    name=models.CharField(max_length=60)
    surname=models.CharField(max_length=60)
    mail=models.CharField(max_length=60)

    faculty=models.ForeignKey(Faculty, on_delete=models.CASCADE)


class Tournament(models.Model):
    game_name=models.CharField(max_length=60)
    season_start=models.DateTimeField()
    season_end=models.DateTimeField()
    team_size=models.IntegerField()


class Team(models.Model):
    is_public=models.BooleanField(default=True)

    tournament=models.ForeignKey(Tournament, on_delete=models.CASCADE)


class Player(models.Model):
    tournament=models.ForeignKey(Tournament, on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    team=models.ForeignKey(Team,on_delete=models.SET_NULL, null=True)


class Match(models.Model):
    created_at=models.DateField()
    expires_at=models.DateField()
    suggested_at=models.DateField(null=True)
    inviting_score=models.IntegerField(null=True)
    guest_score=models.IntegerField(null=True)

    inviting_team=models.ForeignKey(Team, on_delete=models.CASCADE, related_name='inviting_matches')
    guest_team=models.ForeignKey(Team, on_delete=models.CASCADE, related_name='guest_matches')


class ScoreProposition(models.Model):
    inviting_score=models.IntegerField(null=True)
    guest_score=models.IntegerField(null=True)

    suggesting_team=models.ForeignKey(Team, on_delete=models.CASCADE)
    match=models.ForeignKey(Match, on_delete=models.CASCADE)


class PlayerInvite(models.Model):
    expire_date=models.DateField()

    player=models.ForeignKey(Player, on_delete=models.CASCADE)
    team=models.ForeignKey(Team, on_delete=models.CASCADE)


class TeamRequest(models.Model):
    expire_date = models.DateField()

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
