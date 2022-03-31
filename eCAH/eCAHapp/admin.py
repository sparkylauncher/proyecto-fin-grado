from django.contrib import admin

# Register your models here.
from eCAHapp.models import Room, Player, Card

admin.site.register(Room)
admin.site.register(Player)
admin.site.register(Card)