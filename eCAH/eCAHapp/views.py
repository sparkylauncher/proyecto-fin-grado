# Create your views here.
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from random import randint

from eCAHapp.models import Player, Room


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def lobby(request, fullroom='false'):
    Player.objects.all().delete()
    Room.objects.all().delete()
    return render(request, 'lobby.html', {
        'fullroom': fullroom
    })


def contact(request):
    return render(request, 'contact.html')


def nickcheck(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': Player.objects.filter(nickname__iexact=username).exists()
    }
    return JsonResponse(data)


def new_room(request):
    """
    Randomly create a new room, and redirect to it.
    """
    my_new_room = None
    while not my_new_room:
        with transaction.atomic():
            label = str(randint(0, 10))
            if Room.objects.filter(label=label).exists():
                continue
            my_new_room = Room.objects.create(label=label)

    return redirect(created_room, room_name=label)


def created_room(request, room_name):
    max_players = 8

    room = Room.objects.get(label=room_name)
    nplayers = Player.objects.filter(room=room).count()

    if nplayers == max_players:
        return render(request, 'full_room.html', {
            'room_name': room_name,
        })
    else:
        return render(request, 'room.html', {
            'room_name': room_name,
            'variable': "var",
        })
