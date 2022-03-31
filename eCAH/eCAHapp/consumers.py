# chat/consumers.py
import json
import random
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from eCAHapp.models import Player, Room, Card


class ChatConsumer(WebsocketConsumer):

    def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        self.player_disconnect()
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        event_type = self.event_switch(text_data_json['event_type'])

        getattr(self, event_type)(text_data_json)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': event_type + '_notify',
                'info': text_data_json
            }
        )

    def player_connect(self, info):
        self.nickname = info['player_name']
        this_room = Room.objects.get(label=self.room_name)
        this_room.players.create(room=this_room, nickname=self.nickname)

    def player_connect_notify(self, event):
        this_room = Room.objects.get(label=self.room_name)
        players_list = []
        for player in Player.objects.filter(room=this_room):
            players_list.append(player.nickname)

        self.send(text_data=json.dumps({
            'event_type': 'player_connect',
            'player_name': event['info']['player_name'],
            'nplayers': Player.objects.filter(room=this_room).count(),
            'players_list': players_list
        }))

    def player_disconnect(self):
        this_room = Room.objects.get(label=self.room_name)
        Player.objects.filter(nickname=self.nickname).delete()
        nplayers = Player.objects.filter(room=this_room).count()
        if nplayers == 0:
            Room.objects.filter(label=self.room_name).delete()
        else:
            print(self.nickname)
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'player_disconnect_notify',
                    'player_name': self.nickname
                })

    def player_disconnect_notify(self, event):
        this_room = Room.objects.get(label=self.room_name)
        self.send(text_data=json.dumps({
            'event_type': 'player_disconnect',
            'player_name': event["player_name"],
            'nplayers': Player.objects.filter(room=this_room).count()
        }))

    def event_switch(self, event_type):
        event_dict = {
            'player_connect': 'player_connect',
            'game_start': 'game_start',
            'card_played': 'card_played',
            'round_winner': 'round_winner',
            'game_winner': 'game_winner'
        }
        return event_dict.get(event_type)

    def game_start(self, event):
        room = Room.objects.get(label=self.room_name)
        room.game_status = Room.PLAYING
        room.save()
        black_cards = Card.objects.filter(is_black=True).values('text')
        white_cards = Card.objects.filter(is_black=False).values('text')
        event['black_cards'] = []
        event['white_cards'] = []
        for bcard in black_cards:
            event['black_cards'].append(bcard['text'])
        for wcard in white_cards:
            event['white_cards'].append(wcard['text'])

        random.shuffle(event['black_cards'])
        random.shuffle(event['white_cards'])

    def game_start_notify(self, event):
        self.send(text_data=json.dumps({
            'event_type': 'game_start',
            'white_cards': event['info']['white_cards'],
            'black_cards': event['info']['black_cards']
        }))

    def card_played(self, event):
        return

    def card_played_notify(self, event):
        self.send(text_data=json.dumps({
            'event_type': "card_played",
            'card_played': event['info']['card_text'],
            'nickname': event['info']['player_name']
        }))

    def round_winner(self, event):
        return

    def round_winner_notify(self, event):
        print(event);
        self.send(text_data=json.dumps({
            'event_type': "round_winner",
            'nickname': event['info']['player_name']
        }))

    def game_winner(self, event):
        return

    def game_winner_notify(self, event):
        self.send(text_data=json.dumps({
            'event_type': "game_winner",
            'nickname': event['info']['player_name']
        }))