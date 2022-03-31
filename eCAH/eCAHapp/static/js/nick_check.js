        var username=""

        function nick_is_taken(nickname) {
            $.ajax({
                url: '/salas/verificanick/',
                data: {
                  'username': nickname
                },
                dataType: 'json',
                success: function (data) {
                    if(data.is_taken){
                        return true;
                    }else{
                        username=nickname;
                        return false;
                    }
                }
            });
        }

        function get_nick(){
            return nickname;
        }