        function websocket_room_create(){
            return new WebSocket(
                'ws://'
                + window.location.host
                + '/ws/salas/'
                + roomName
                + '/'
            );
        }