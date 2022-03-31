from django.db import models

class Room(models.Model):
    WAITING_START = 'WAITING_START'
    PLAYING = 'PLAYING'
    STARTED_BUT_NEED_PLAYERS = 'STARTED_BUT_NEED_PLAYERS'
    GAME_FINISH = 'GAME_FINISH'

    GAME_STATUS = [
        (WAITING_START, 'WAITING_START'),
        (PLAYING, 'PLAYING'),
        (STARTED_BUT_NEED_PLAYERS, 'STARTED_BUT_NEED_PLAYERS'),
        (GAME_FINISH, 'GAME_FINISH')
    ]

    name = models.TextField()
    label = models.SlugField(unique=True)
    game_status = models.CharField(choices=GAME_STATUS, default=WAITING_START, max_length=50)

    def __unicode__(self):
        return self.label


class Card(models.Model):
    text = models.TextField()
    is_black = models.BooleanField()


class Player(models.Model):
    room = models.ForeignKey(Room, related_name='players', on_delete=models.CASCADE)
    nickname = models.TextField()
